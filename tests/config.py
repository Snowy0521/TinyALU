from alu_common import Ops
from dataclasses import dataclass

AGENT_MODE_ACTIVE = "active"
AGENT_MODE_PASSIVE = "passive"
AGENT_MODE = AGENT_MODE_ACTIVE


@dataclass(frozen=True)
class AgentConfig:
    name: str
    mode: str
    bfm_key: str


# Multi-agent ready config:
# - Add more AgentConfig entries to scale out.
# - Each agent should use a unique bfm_key when bound to different BFMs.
AGENT_CONFIGS = [
    AgentConfig(name="agent0", mode=AGENT_MODE, bfm_key="BFM_AGENT0"),
]
DEFAULT_BFM_KEY = AGENT_CONFIGS[0].bfm_key


AA_BINS = [0, 1, 127, 128, 254, 255]
BB_BINS = [0, 1, 127, 128, 254, 255]

MAX_COVERAGE_ITERS = 30
RANDOM_SEQ_BATCH_ITEMS = 100

RANDOM_NOOP_PROBABILITY = 0.08
RANDOM_EDGE_BINS_PROBABILITY = 0.7
RANDOM_NON_NOOP_OPS = [Ops.ADD, Ops.AND, Ops.XOR, Ops.MUL]
RANDOM_NON_NOOP_OP_WEIGHTS = [0.3, 0.3, 0.2, 0.2]
