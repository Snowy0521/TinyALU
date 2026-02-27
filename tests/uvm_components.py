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
    AGENT_MODE_ACTIVE,
    AGENT_MODE_PASSIVE,
    AGENT_CONFIGS,
    MAX_COVERAGE_ITERS,
)
from coverage_model import AluCoverage
from sequences import RandomSeq


class AluDriver(uvm_driver):
    """Driver: drives transactions to the DUT using BFM"""

    def build_phase(self):
        super().build_phase()
        self.agent_cfg = ConfigDB().get(self, "", "AGENT_CFG")
        self.bfm = ConfigDB().get(self, "", self.agent_cfg.bfm_key)
        self.logger.info(f"Got BFM from ConfigDB key '{self.agent_cfg.bfm_key}'")

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
        self.agent_cfg = ConfigDB().get(self, "", "AGENT_CFG")
        self.bfm = ConfigDB().get(self, "", self.agent_cfg.bfm_key)
        self.logger.info(
            f"Monitor got BFM from ConfigDB key '{self.agent_cfg.bfm_key}'"
        )

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
    def build_phase(self):
        self.cfg = ConfigDB().get(self, "", "AGENT_CFG")
        self.seqr = None
        self.driver = None
        self.monitor = AluMonitor("monitor", self)
        if self.is_active_mode():
            self.seqr = uvm_sequencer("seqr", self)
            self.driver = AluDriver("driver", self)
        else:
            self.logger.info(f"{self.get_full_name()} in passive mode: monitor-only")

    def is_active_mode(self):
        mode = str(self.cfg.mode).lower()
        if mode not in (AGENT_MODE_ACTIVE, AGENT_MODE_PASSIVE):
            raise ValueError(
                f"Invalid agent mode={self.cfg.mode}. "
                f"Use {AGENT_MODE_ACTIVE!r} or {AGENT_MODE_PASSIVE!r}."
            )
        return mode == AGENT_MODE_ACTIVE

    def connect_phase(self):
        if self.is_active_mode():
            self.driver.seq_item_port.connect(self.seqr.seq_item_export)


class AluEnv(uvm_env):
    def build_phase(self):
        self.agents = {}
        self.scoreboards = {}
        self.coverages = {}

        if len(AGENT_CONFIGS) == 0:
            raise ValueError("AGENT_CONFIGS must define at least one agent")

        for cfg in AGENT_CONFIGS:
            ConfigDB().set(self, cfg.name, "AGENT_CFG", cfg)
            ConfigDB().set(self, f"{cfg.name}.*", "AGENT_CFG", cfg) # Subcomponents can also access via hierarchical wildcard
            agent = AluAgent(cfg.name, self)
            scoreboard = AluScoreboard(f"{cfg.name}_scoreboard", self)
            coverage = AluCoverage(f"{cfg.name}_coverage", self)

            self.agents[cfg.name] = agent
            self.scoreboards[cfg.name] = scoreboard
            self.coverages[cfg.name] = coverage

    def connect_phase(self):
        for agent_name, agent in self.agents.items():
            agent.monitor.ap.connect(self.scoreboards[agent_name].monitor_export)
            agent.monitor.ap.connect(self.coverages[agent_name].analysis_export)

    def get_active_sequencers(self):
        active_seqrs = {}
        for agent_name, agent in self.agents.items():
            if agent.is_active_mode():
                active_seqrs[agent_name] = agent.seqr
        return active_seqrs


class AluTest(uvm_test):
    def build_phase(self):
        self.env = AluEnv("env", self)

    async def run_phase(self):
        self.raise_objection()

        active_seqrs = self.env.get_active_sequencers()
        if len(active_seqrs) == 0:
            self.logger.info("Passive agent mode: skipping sequence-driven stimulus")
            self.drop_objection()
            return

        print("\n[TEST] Random with coverage closure (multi-agent)")
        iteration = 0
        while not AluCoverage.coverage_closure():
            iteration += 1
            if iteration > MAX_COVERAGE_ITERS:
                self.logger.error(
                    f"Coverage did not converge after {MAX_COVERAGE_ITERS} iterations"
                )
                break

            for agent_name, seqr in active_seqrs.items():
                seq = RandomSeq(f"{agent_name}_random_{iteration}")
                await seq.start(seqr)

            covered_bins, total_bins, percentage = AluCoverage.get_overall_coverage()
            self.logger.info(
                f"Coverage after iter {iteration}: {percentage:.2f}% "
                f"({covered_bins}/{total_bins})"
            )

        self.drop_objection()
