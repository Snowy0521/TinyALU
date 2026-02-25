import cocotb
from pyuvm import *
import random
from tinyalu_bfm import TinyAluBfm
from cocotb.clock import Clock
from cocotb_coverage.coverage import coverage_section, CoverPoint, CoverCross
from cocotb_coverage.coverage import coverage_db

# Define ALU operations as an enumeration
class Ops(IntEnum):
    NOOP = 0
    ADD  = 1
    AND  = 2
    XOR  = 3
    MUL  = 4

# 1. 定义采样装饰器
alu_cov_obj = coverage_section(
    CoverPoint("top.op", 
               xf=lambda item: item.op, 
               bins=list(Ops)), 

    CoverPoint("top.aa", 
               xf=lambda item: item.aa,  
               bins=[0, 1, 127, 128, 254, 255]),
    
    CoverPoint("top.bb", 
               xf=lambda item: item.bb, 
               bins=[0, 1, 127, 128, 254, 255]),

    CoverPoint("top.add_carry",
               xf=lambda item: ((item.aa + item.bb) > 0xFF) if item.op == Ops.ADD else None,
               bins=[True, False]),

    CoverPoint("top.mul_high_byte_nonzero",
               xf=lambda item: ((item.aa * item.bb) > 0xFF) if item.op == Ops.MUL else None,
               bins=[True, False]),

    CoverPoint("top.and_zero",
               xf=lambda item: ((item.aa & item.bb) == 0) if item.op == Ops.AND else None,
               bins=[True, False]),

    CoverPoint("top.xor_same",
               xf=lambda item: (item.aa == item.bb) if item.op == Ops.XOR else None,
               bins=[True, False]),
    
    CoverCross("top.op_cross_aa", 
               items=["top.op", "top.aa"]),

    CoverCross("top.op_cross_aa_bb", 
               items=["top.op", "top.aa", "top.bb"])
)


def sample_func(item):
    return item

sample_alu_coverage = alu_cov_obj(sample_func)

class AluCoverage(uvm_subscriber):
    """Coverage collector: collects coverage data for ALU operations and operand combinations"""
    def __init__(self, name, parent):
        super().__init__(name, parent)
    
    def write(self, item):
        """Called by the monitor to sample coverage for each transaction"""
        sample_alu_coverage(item)  # Sample the coverage with the transaction item

    @staticmethod
    def get_overall_coverage():
        total_bins = 0
        covered_bins = 0
        for cover_point in coverage_db:
            cp = coverage_db[cover_point]
            total_bins += cp.size
            covered_bins += cp.coverage
        percentage = (covered_bins / total_bins * 100) if total_bins > 0 else 0.0
        return covered_bins, total_bins, percentage

    @classmethod
    def coverage_closure(cls):
        covered_bins, total_bins, _ = cls.get_overall_coverage()
        return total_bins > 0 and covered_bins == total_bins

    def report_phase(self):
        print("\n" + "=" * 60)
        print("ALU FUNCTIONAL COVERAGE REPORT")
        print("=" * 60)
        
        try:
            # Print overall coverage
            total_bins = 0
            covered_bins = 0
            
            # Iterate through all coverage points
            for cover_point in coverage_db:
                cp_name = cover_point
                cp_size = coverage_db[cover_point].size
                cp_coverage = coverage_db[cover_point].coverage
                cp_detailed_coverage = coverage_db[cover_point].detailed_coverage
                
                total_bins += cp_size
                covered_bins += cp_coverage
                
                percentage = (cp_coverage / cp_size * 100) if cp_size > 0 else 0
                print(f"{cp_name:30} : {percentage:6.2f}% ({cp_coverage}/{cp_size})")
                
                # Print detailed bin coverage for each cover point
                if hasattr(coverage_db[cover_point], 'bins') and len(coverage_db[cover_point].bins) < 20:
                    for bin_name, bin_hit in cp_detailed_coverage.items():
                        status = "HIT" if bin_hit > 0 else "MISS"
                        print(f"  {str(bin_name):25} : {status:4} (hits: {bin_hit})")
            
            # Print total coverage
            print("-" * 60)
            overall_percentage = (covered_bins / total_bins * 100) if total_bins > 0 else 0
            print(f"{'OVERALL COVERAGE':30} : {overall_percentage:6.2f}% ({covered_bins}/{total_bins})")
            
        except Exception as e:
            print(f"Error accessing coverage: {e}")
            print("Attempting alternative method...")
        
        print("=" * 60 + "\n")

    
class AluSeqItem(uvm_sequence_item):
    """ALU transaction item"""
    def __init__(self, name, op, aa, bb):
        super().__init__(name)
        self.op = op
        self.aa = aa
        self.bb = bb
        self.result = 0

    def __str__(self):
        return f"{self.get_name()} : op={self.op.name} aa=0x{self.aa:02x} bb=0x{self.bb:02x} result=0x{self.result:04x}"

# Define bins for operand values, focusing on edge cases and typical values
AA_BINS = [0, 1, 127, 128, 254, 255]
BB_BINS = [0, 1, 127, 128, 254, 255]

# Simple helper function to send a single item through the sequence, used for testing
def calc_expected(op, aa, bb):
    if op == Ops.ADD:
        return (aa + bb) & 0xFFFF
    if op == Ops.AND:
        return aa & bb
    if op == Ops.XOR:
        return aa ^ bb
    if op == Ops.MUL:
        return (aa * bb) & 0xFFFF
    return 0

async def send_item(seq, i, op, aa, bb):
    item = AluSeqItem(f"item_{i}", op, aa, bb)
    print(f"\n[{i}] Sending: op={op.name:4s} A=0x{aa:02x} B=0x{bb:02x}")
    await seq.start_item(item)
    await seq.finish_item(item)
    print(f"[{i}] Result:  0x{item.result:04x}")
    expected = calc_expected(op, aa, bb)
    status = "PASS" if item.result == expected else "FAIL"
    print(f"[{i}] {status}:   op={op.name:4s} A=0x{aa:02x} B=0x{bb:02x} "
          f"Got=0x{item.result:04x} Exp=0x{expected:04x}")
    return item


class SmokeSeq(uvm_sequence):
    """Smoke sequence: sends a small number of fixed transactions to quickly check basic functionality"""
    async def body(self):
        print("\n" + "=" * 60)
        print("SEQUENCE: SmokeSeq")
        print("=" * 60)
        cases = [
            (Ops.NOOP, 0x00, 0x00),
            (Ops.ADD,  0x01, 0x02),
            (Ops.AND,  0xFF, 0x0F),
            (Ops.XOR,  0xAA, 0x55),
            (Ops.MUL,  0x0F, 0x0F),
        ]
        for i, (op, aa, bb) in enumerate(cases):
            await send_item(self, i, op, aa, bb)


class BoundarySeq(uvm_sequence):
    """Boundary sequence: tests edge cases and boundary conditions for ALU operations"""
    async def body(self):
        print("\n" + "=" * 60)
        print("SEQUENCE: BoundarySeq")
        print("=" * 60)
        i = 0
        for op in list(Ops):
            for aa in AA_BINS:
                for bb in BB_BINS:
                    await send_item(self, i, op, aa, bb)
                    i += 1

class BackToBackSeq(uvm_sequence):
    """Back-to-back sequence: sends a mix of operations in quick succession to test pipeline and timing behavior"""
    num_items = 20
    async def body(self):
        print("\n" + "=" * 60)
        print("SEQUENCE: BackToBackSeq")
        print("=" * 60)
        for i in range(self.num_items):
            op = random.choice([Ops.ADD, Ops.MUL])   
            aa = random.choice(AA_BINS)
            bb = random.choice(BB_BINS)
            await send_item(self, i, op, aa, bb)

class ResetSeq(uvm_sequence):
    """Reset sequence: tests behavior when reset is asserted in the middle of operations and immediately after reset"""
    async def body(self):
        print("\n" + "=" * 60)
        print("SEQUENCE: ResetSeq")
        print("=" * 60)

        bfm = uvm_root()._bfm

        # 场景1：MUL 中途复位
        print("[ResetSeq] Scenario 1: Reset during MUL operation")
        item = AluSeqItem("reset_mid", Ops.MUL, 0xFF, 0xFF)
        await self.start_item(item)
        await self.finish_item(item)
        await bfm.reset()                              
        await bfm.check_reset_state()

        # 场景2：复位后立刻发送 ADD
        print("\n[ResetSeq] Scenario 2: Send ADD immediately after reset")
        await send_item(self, 0, Ops.ADD, 0x01, 0x01)

        # 场景3：连续多次复位
        print("\n[ResetSeq] Scenario 3: Continuous resets")
        for _ in range(3):
            await bfm.reset()
        await send_item(self, 1, Ops.AND, 0xFF, 0xFF)


class RandomSeq(uvm_sequence):
    """Random sequence: generates random transactions"""
    num_items = 0

    async def body(self):
        print("\n" + "=" * 60)
        print(f"SEQUENCE: Generating {self.num_items} random transactions")
        print("=" * 60)
        
        for i in range(self.num_items):
            if random.random() < 0.08:          # 8% 概率发 NOOP
                op = Ops.NOOP
                aa = random.choice(AA_BINS)
                bb = random.choice(BB_BINS)
            else:
                op = random.choices(
                    list(Ops)[1:],
                    weights=[0.3, 0.3, 0.2, 0.2]   # 在非 NOOP 中保持原比例
                )[0]
                if random.random() < 0.7:
                    aa = random.choice(AA_BINS)
                    bb = random.choice(BB_BINS)
                else:
                    aa = random.randint(0, 0xFF)
                    bb = random.randint(0, 0xFF)
            await send_item(self, i, op, aa, bb)
            
        print("\n" + "=" * 60)
        print("SEQUENCE: All transactions completed")
        print("=" * 60 + "\n")

class AluDriver(uvm_driver):
    """Driver: drives transactions to the DUT using BFM"""
    def build_phase(self):
        super().build_phase()

        # Obtain BFM reference from uvm_root
        if hasattr(uvm_root(), '_bfm'):
            self.bfm = uvm_root()._bfm
            self.logger.info("Got BFM from uvm_root()._bfm")
        else:
            self.logger.error("BFM not found in uvm_root()._bfm")
            raise Exception("BFM not found")

    async def run_phase(self):
        self.logger.info("Driver run_phase started")
        
        while True:
            # Obtain the next item from the sequencer
            item = await self.seq_item_port.get_next_item()
            
            # Use BFM to send the operation and get the result
            try:
                result = await self.bfm.send_op(item.op.value, item.aa, item.bb)
                item.result = result 
                self.logger.info(f"Driver sent: op={item.op.name} aa=0x{item.aa:02x} bb=0x{item.bb:02x} result=0x{item.result:04x}")
            except Exception as e:
                self.logger.error(f"Error in send_op: {e}")
                item.result = 0
            
            # Indicate that the item is done
            self.seq_item_port.item_done()

class AluScoreboard(uvm_scoreboard):
    """Scoreboard: checks results against expected values"""
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.passed = 0
        self.failed = 0
    
    def build_phase(self):
        super().build_phase()
        self.monitor_fifo = uvm_tlm_analysis_fifo("monitor_fifo", self)
        self.monitor_export = self.monitor_fifo.analysis_export

    async def run_phase(self):
        while True:
            monitor_item = await self.monitor_fifo.get()
            self.check_result(monitor_item)

    def check_result(self, item):
        """Check a single monitored transaction"""
        if item.op == Ops.NOOP:
            return

        expected = self.calculate_expected(item)
        actual = item.result

        if actual != expected:
            self.logger.error(f"FAIL: {item.op.name} A=0x{item.aa:02x} B=0x{item.bb:02x} "
                              f"Got=0x{actual:04x} Exp=0x{expected:04x}")
            self.failed += 1
        else:
            self.passed += 1

    def calculate_expected(self, item):
        return calc_expected(item.op, item.aa, item.bb)

    def report_phase(self):
        """final report"""
        print("\n" + "=" * 60)
        print("FINAL RESULTS")
        print("=" * 60)
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Total:  {self.passed + self.failed}")
        
        if self.failed == 0 and self.passed > 0:
            print("\nALL TESTS PASSED!")
        elif self.failed > 0:
            print(f"\n{self.failed} TEST(S) FAILED")
        
        print("=" * 60 + "\n")

class AluMonitor(uvm_component):
    """Monitor: """
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.ap = uvm_analysis_port("ap", self)
    
    def build_phase(self):
        if hasattr(uvm_root(), '_bfm'):
            self.bfm = uvm_root()._bfm
            self.logger.info("Monitor got BFM from uvm_root()._bfm")
        else:
            self.logger.error("Monitor could not find BFM in uvm_root()._bfm")
            raise Exception("BFM not found for Monitor")

    async def run_phase(self):
        self.logger.info("Monitor run_phase started")
        while True:
            obs_data = await self.bfm.get_result()
            op = Ops(obs_data['op'])

            if op == Ops.NOOP:
                if obs_data.get('done_width', 0) != 0:
                    self.logger.error("NOOP should never drive done high")
            else:
                expected_latency = 3 if op == Ops.MUL else 1
                actual_latency = obs_data.get('latency')
                if actual_latency != expected_latency:
                    self.logger.error(
                        f"Timing FAIL: {op.name} expected latency={expected_latency}, got latency={actual_latency}"
                    )

                if obs_data.get('done_width', 1) != 1:
                    self.logger.error(f"done pulse width FAIL: {op.name} width={obs_data.get('done_width')}")

            item = AluSeqItem("mon_item", 
                              op,
                              obs_data['aa'], 
                              obs_data['bb'])
            item.result = obs_data['result']

            self.ap.write(item) # Send observed item to scoreboard

class AluAgent(uvm_agent):
    """Agent: contains driver and monitor, connects them to the sequencer and scoreboard"""
    def build_phase(self):
        self.seqr = uvm_sequencer("seqr", self)
        self.driver = AluDriver("driver", self)
        self.monitor = AluMonitor("monitor", self)

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)

class AluEnv(uvm_env):
    """Environment: contains the agent and scoreboard, connects them together"""
    def build_phase(self):
        self.agent = AluAgent("agent", self)
        self.scoreboard = AluScoreboard("scoreboard", self)
        self.coverage = AluCoverage("coverage", self)
    
    def connect_phase(self):
        self.agent.monitor.ap.connect(self.scoreboard.monitor_export)
        self.agent.monitor.ap.connect(self.coverage.analysis_export) # Connect monitor to coverage collector

class AluTest(uvm_test):
    """Test: top-level test class, runs the sequence and manages the environment"""
    def build_phase(self):
        self.env = AluEnv("env", self)

    async def run_phase(self):
        self.raise_objection()
        
        seqr = self.env.agent.seqr
        max_iters = 30
        batch_items = 100

        #print("\n[TEST] Phase 1: Smoke")
        #await SmokeSeq("smoke").start(seqr)

        #print("\n[TEST] Phase 2: Boundary")
        #await BoundarySeq("boundary").start(seqr)

        #print("\n[TEST] Phase 3: BackToBack")
        #await BackToBackSeq("b2b").start(seqr)

        #print("\n[TEST] Phase 4: Reset")
        #await ResetSeq("reset").start(seqr)

        print("\n[TEST] Phase 5: Random with coverage closure")
        iteration = 0
        while not AluCoverage.coverage_closure():
            iteration += 1
            if iteration > max_iters:
                self.logger.error(
                    f"Coverage did not converge after {max_iters} iterations"
                )
                break

            seq = RandomSeq(f"random_{iteration}")
            seq.num_items = batch_items
            await seq.start(seqr)

            covered_bins, total_bins, percentage = AluCoverage.get_overall_coverage()
            self.logger.info(
                f"Coverage after iter {iteration}: "
                f"{percentage:.2f}% ({covered_bins}/{total_bins})"
            )
        
        self.drop_objection()

@cocotb.test()
async def test_tinyalu(dut):
    """
    Top-level test function: initializes BFM, starts clock, runs UVM test
    """
    print("\n" + "=" * 70)
    print(" " * 20 + "TINYALU UVM TESTBENCH")
    print("=" * 70)
    print(f"DUT: {dut._name}")
    print("=" * 70 + "\n")
    
    # 1. Create and start clock
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    print("Clock started (10ns period, 100MHz)")
    
    # 2. Initialize BFM and reset DUT
    bfm = TinyAluBfm(dut)
    await bfm.reset()
    print("DUT reset completed")
    
    # 3. Store BFM reference in uvm_root for access by UVM components
    uvm_root()._bfm = bfm
    print("BFM stored in uvm_root()._bfm")
    
    print("\n" + "Starting UVM test..." + "\n")
    
    # 4. Run the UVM test
    await uvm_root().run_test("AluTest")
    
    print("\n" + "=" * 70)
    print(" " * 25 + "TEST COMPLETE")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    print(__doc__)
    print("\nRun with:")
    print("  make clean")
    print("  make SIM=verilator WAVE=1")
