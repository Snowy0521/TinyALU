from enum import IntEnum

from pyuvm import uvm_sequence_item


class Ops(IntEnum):
    NOOP = 0
    ADD = 1
    AND = 2
    XOR = 3
    MUL = 4


class AluSeqItem(uvm_sequence_item):
    """ALU transaction item"""

    def __init__(self, name, op, aa, bb):
        super().__init__(name)
        self.op = op
        self.aa = aa
        self.bb = bb
        self.result = 0

    def __str__(self):
        return (
            f"{self.get_name()} : op={self.op.name} aa=0x{self.aa:02x} "
            f"bb=0x{self.bb:02x} result=0x{self.result:04x}"
        )


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
