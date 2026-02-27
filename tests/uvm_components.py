from pyuvm import (
    ConfigDB,
    uvm_agent,
    uvm_analysis_port,
    uvm_component,
    uvm_driver,
    uvm_env,
    uvm_scoreboard,
    uvm_sequencer,
    uvm_test,
    uvm_tlm_analysis_fifo,
)

from alu_common import AluSeqItem, Ops, calc_expected
from config import (
    AGENT_MODE,
    AGENT_MODE_ACTIVE,
    AGENT_MODE_PASSIVE,
    MAX_COVERAGE_ITERS,
    RANDOM_SEQ_BATCH_ITEMS,
)
from coverage_model import AluCoverage
from sequences import RandomSeq


class AluDriver(uvm_driver):
    """Driver: drives transactions to the DUT using BFM"""

    def build_phase(self):
        super().build_phase()
        self.bfm = ConfigDB().get(self, "", "BFM")
        self.logger.info("Got BFM from ConfigDB key 'BFM'")

    async def run_phase(self):
        self.logger.info("Driver run_phase started")
        while True:
            item = await self.seq_item_port.get_next_item()
            try:
                result = await self.bfm.send_op(item.op.value, item.aa, item.bb)
                item.result = result
                self.logger.info(
                    f"Driver sent: op={item.op.name} aa=0x{item.aa:02x} "
                    f"bb=0x{item.bb:02x} result=0x{item.result:04x}"
                )
            except Exception as e:
                self.logger.error(f"Error in send_op: {e}")
                item.result = 0
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
        if item.op == Ops.NOOP:
            return

        expected = calc_expected(item.op, item.aa, item.bb)
        actual = item.result
        if actual != expected:
            self.logger.error(
                f"FAIL: {item.op.name} A=0x{item.aa:02x} B=0x{item.bb:02x} "
                f"Got=0x{actual:04x} Exp=0x{expected:04x}"
            )
            self.failed += 1
        else:
            self.passed += 1

    def report_phase(self):
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
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.ap = uvm_analysis_port("ap", self)

    def build_phase(self):
        self.bfm = ConfigDB().get(self, "", "BFM")
        self.logger.info("Monitor got BFM from ConfigDB key 'BFM'")

    async def run_phase(self):
        self.logger.info("Monitor run_phase started")
        while True:
            obs_data = await self.bfm.get_result()
            op = Ops(obs_data["op"])

            if op == Ops.NOOP:
                if obs_data.get("done_width", 0) != 0:
                    self.logger.error("NOOP should never drive done high")
            else:
                expected_latency = 3 if op == Ops.MUL else 1
                actual_latency = obs_data.get("latency")
                if actual_latency != expected_latency:
                    self.logger.error(
                        f"Timing FAIL: {op.name} expected latency={expected_latency}, "
                        f"got latency={actual_latency}"
                    )
                if obs_data.get("done_width", 1) != 1:
                    self.logger.error(
                        f"done pulse width FAIL: {op.name} width={obs_data.get('done_width')}"
                    )

            item = AluSeqItem("mon_item", op, obs_data["aa"], obs_data["bb"])
            item.result = obs_data["result"]
            self.ap.write(item)


class AluAgent(uvm_agent):
    def is_active_mode(self):
        mode = str(AGENT_MODE).lower()
        if mode not in (AGENT_MODE_ACTIVE, AGENT_MODE_PASSIVE):
            raise ValueError(
                f"Invalid AGENT_MODE={AGENT_MODE}. "
                f"Use {AGENT_MODE_ACTIVE!r} or {AGENT_MODE_PASSIVE!r}."
            )
        return mode == AGENT_MODE_ACTIVE

    def build_phase(self):
        self.seqr = None
        self.driver = None
        self.monitor = AluMonitor("monitor", self)
        if self.is_active_mode():
            self.seqr = uvm_sequencer("seqr", self)
            self.driver = AluDriver("driver", self)
        else:
            self.logger.info("AluAgent in passive mode: monitor-only")

    def connect_phase(self):
        if self.is_active_mode():
            self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class AluEnv(uvm_env):
    def build_phase(self):
        self.agent = AluAgent("agent", self)
        self.scoreboard = AluScoreboard("scoreboard", self)
        self.coverage = AluCoverage("coverage", self)

    def connect_phase(self):
        self.agent.monitor.ap.connect(self.scoreboard.monitor_export)
        self.agent.monitor.ap.connect(self.coverage.analysis_export)


class AluTest(uvm_test):
    def build_phase(self):
        self.env = AluEnv("env", self)

    async def run_phase(self):
        self.raise_objection()

        if not self.env.agent.is_active_mode():
            self.logger.info("Passive agent mode: skipping sequence-driven stimulus")
            self.drop_objection()
            return

        seqr = self.env.agent.seqr
        print("\n[TEST] Phase 5: Random with coverage closure")
        iteration = 0
        while not AluCoverage.coverage_closure():
            iteration += 1
            if iteration > MAX_COVERAGE_ITERS:
                self.logger.error(
                    f"Coverage did not converge after {MAX_COVERAGE_ITERS} iterations"
                )
                break

            seq = RandomSeq(f"random_{iteration}")
            seq.num_items = RANDOM_SEQ_BATCH_ITEMS
            await seq.start(seqr)

            covered_bins, total_bins, percentage = AluCoverage.get_overall_coverage()
            self.logger.info(
                f"Coverage after iter {iteration}: {percentage:.2f}% "
                f"({covered_bins}/{total_bins})"
            )

        self.drop_objection()
