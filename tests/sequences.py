import random

from pyuvm import ConfigDB, uvm_sequence

from alu_common import AluSeqItem, Ops, calc_expected
from config import (
    AA_BINS,
    BB_BINS,
    DEFAULT_BFM_KEY,
    RANDOM_EDGE_BINS_PROBABILITY,
    RANDOM_NON_NOOP_OP_WEIGHTS,
    RANDOM_NON_NOOP_OPS,
    RANDOM_NOOP_PROBABILITY,
    RANDOM_SEQ_BATCH_ITEMS,
)


async def send_item(seq, i, op, aa, bb):
    item = AluSeqItem(f"item_{i}", op, aa, bb)
    print(f"\n[{i}] Sending: op={op.name:4s} A=0x{aa:02x} B=0x{bb:02x}")
    await seq.start_item(item)
    await seq.finish_item(item)
    print(f"[{i}] Result:  0x{item.result:04x}")
    expected = calc_expected(op, aa, bb)
    status = "PASS" if item.result == expected else "FAIL"
    print(
        f"[{i}] {status}:   op={op.name:4s} A=0x{aa:02x} B=0x{bb:02x} "
        f"Got=0x{item.result:04x} Exp=0x{expected:04x}"
    )
    return item


class SmokeSeq(uvm_sequence):
    """Smoke sequence: sends a small number of fixed transactions to quickly check basic functionality"""

    async def body(self):
        print("\n" + "=" * 60)
        print("SEQUENCE: SmokeSeq")
        print("=" * 60)
        cases = [
            (Ops.NOOP, 0x00, 0x00),
            (Ops.ADD, 0x01, 0x02),
            (Ops.AND, 0xFF, 0x0F),
            (Ops.XOR, 0xAA, 0x55),
            (Ops.MUL, 0x0F, 0x0F),
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

        bfm = ConfigDB().get(self, "", DEFAULT_BFM_KEY)

        print("[ResetSeq] Scenario 1: Reset during MUL operation")
        item = AluSeqItem("reset_mid", Ops.MUL, 0xFF, 0xFF)
        await self.start_item(item)
        await self.finish_item(item)
        await bfm.reset()
        await bfm.check_reset_state()

        print("\n[ResetSeq] Scenario 2: Send ADD immediately after reset")
        await send_item(self, 0, Ops.ADD, 0x01, 0x01)

        print("\n[ResetSeq] Scenario 3: Continuous resets")
        for _ in range(3):
            await bfm.reset()
        await send_item(self, 1, Ops.AND, 0xFF, 0xFF)


class RandomSeq(uvm_sequence):
    """Random sequence: generates random transactions"""

    num_items = RANDOM_SEQ_BATCH_ITEMS

    async def body(self):
        print("\n" + "=" * 60)
        print(f"SEQUENCE: Generating {self.num_items} random transactions")
        print("=" * 60)

        for i in range(self.num_items):
            if random.random() < RANDOM_NOOP_PROBABILITY:
                op = Ops.NOOP
                aa = random.choice(AA_BINS)
                bb = random.choice(BB_BINS)
            else:
                op = random.choices(
                    RANDOM_NON_NOOP_OPS,
                    weights=RANDOM_NON_NOOP_OP_WEIGHTS,
                )[0]
                if random.random() < RANDOM_EDGE_BINS_PROBABILITY:
                    aa = random.choice(AA_BINS)
                    bb = random.choice(BB_BINS)
                else:
                    aa = random.randint(0, 0xFF)
                    bb = random.randint(0, 0xFF)
            await send_item(self, i, op, aa, bb)

        print("\n" + "=" * 60)
        print("SEQUENCE: All transactions completed")
        print("=" * 60 + "\n")
