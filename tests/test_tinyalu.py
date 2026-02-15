import cocotb
from pyuvm import *
import random
from tinyalu_bfm import TinyAluBfm
from cocotb.clock import Clock

# Define ALU operations as an enumeration
class Ops(IntEnum):
    NOOP = 0
    ADD  = 1
    AND  = 2
    XOR  = 3
    MUL  = 4

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

class AluSeq(uvm_sequence):
    """ALU sequence: generates random transactions"""
    num_items = 10
    async def body(self):
        print("\n" + "=" * 60)
        print(f"SEQUENCE: Generating {self.num_items} random transactions")
        print("=" * 60)
        
        for i in range(self.num_items):
            op = random.choices(list(Ops)[1:], weights=[0.3, 0.3, 0.2, 0.2])[0] # Exclude NOOP from random ops
            aa = random.choice([0x00, 0xFF, random.randint(1, 0xFE)]) # Random A with edge cases prioritized
            bb = random.choice([0x00, 0xFF, random.randint(1, 0xFE)])
            item = AluSeqItem(f"item_{i}", op, aa, bb)
            
            print(f"\n[{i}] Sending: op={op.name:4s} A=0x{aa:02x} B=0x{bb:02x}")
            
            await self.start_item(item)
            await self.finish_item(item)
            
            print(f"[{i}] Result:  0x{item.result:04x}")
        
        print("\n" + "=" * 60)
        print("SEQUENCE: All transactions completed")
        print("=" * 60 + "\n")

class AluDriver(uvm_driver):
    """Driver: drives transactions to the DUT using BFM"""
    def build_phase(self):
        super().build_phase()
        self.ap = uvm_analysis_port("ap", self) # Analysis port to send results to scoreboard

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
                self.ap.write(item)  
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
        self.driver_fifo = uvm_tlm_analysis_fifo("driver_fifo", self) # FIFO to receive items from the driver
        self.monitor_fifo = uvm_tlm_analysis_fifo("monitor_fifo", self)
        self.driver_export = self.driver_fifo.analysis_export
        self.monitor_export = self.monitor_fifo.analysis_export

    async def run_phase(self):
        while True:
            driver_item = await self.driver_fifo.get()
            monitor_item = await self.monitor_fifo.get()
            
            self.compare_items(driver_item, monitor_item)
    
    def compare_items(self, d_item, m_item):
        if d_item.op == Ops.NOOP:
            return

        # Expected value calculation based on driver item
        expected = self.calculate_expected(d_item)
        
        # Actual value from monitor item
        actual = m_item.result

        # Compare and log results
        if actual != expected:
            self.logger.error(f"FAIL: {d_item.op.name} A=0x{d_item.aa:02x} B=0x{d_item.bb:02x} "
                              f"Got=0x{actual:04x} Exp=0x{expected:04x}")
            self.failed += 1
        else:
            self.logger.info(f"PASS: {d_item.op.name} A=0x{d_item.aa:02x} B=0x{d_item.bb:02x} Result=0x{actual:04x}")
            self.passed += 1

    def calculate_expected(self, item):
        if item.op == Ops.ADD: return (item.aa + item.bb) & 0xFFFF
        if item.op == Ops.AND: return item.aa & item.bb
        if item.op == Ops.XOR: return item.aa ^ item.bb
        if item.op == Ops.MUL: return (item.aa * item.bb) & 0xFFFF
        return 0

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

            item = AluSeqItem("mon_item", 
                              Ops(obs_data['op']), 
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
    
    def connect_phase(self):
        self.agent.driver.ap.connect(self.scoreboard.driver_export)
        self.agent.monitor.ap.connect(self.scoreboard.monitor_export)

class AluTest(uvm_test):
    """Test: top-level test class, runs the sequence and manages the environment"""
    def build_phase(self):
        self.env = AluEnv("env", self)

    async def run_phase(self):
        self.raise_objection()
        
        print("\n" + "=" * 60)
        print("TEST: Running main sequence")
        print("=" * 60)
        
        # Start the main sequence
        seq = AluSeq("main_seq")
        await seq.start(self.env.agent.seqr)
        
        print("\n" + "=" * 60)
        print("TEST: Sequence completed")
        print("=" * 60)
        
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