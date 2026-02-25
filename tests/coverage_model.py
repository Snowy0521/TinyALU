from cocotb_coverage.coverage import CoverCross, CoverPoint, coverage_db, coverage_section
from pyuvm import uvm_subscriber

from alu_common import Ops
from config import AA_BINS, BB_BINS


alu_cov_obj = coverage_section(
    CoverPoint("top.op", xf=lambda item: item.op, bins=list(Ops)),
    CoverPoint("top.aa", xf=lambda item: item.aa, bins=AA_BINS),
    CoverPoint("top.bb", xf=lambda item: item.bb, bins=BB_BINS),
    CoverPoint(
        "top.add_carry",
        xf=lambda item: ((item.aa + item.bb) > 0xFF) if item.op == Ops.ADD else None,
        bins=[True, False],
    ),
    CoverPoint(
        "top.mul_high_byte_nonzero",
        xf=lambda item: ((item.aa * item.bb) > 0xFF) if item.op == Ops.MUL else None,
        bins=[True, False],
    ),
    CoverPoint(
        "top.and_zero",
        xf=lambda item: ((item.aa & item.bb) == 0) if item.op == Ops.AND else None,
        bins=[True, False],
    ),
    CoverPoint(
        "top.xor_same",
        xf=lambda item: (item.aa == item.bb) if item.op == Ops.XOR else None,
        bins=[True, False],
    ),
    CoverCross("top.op_cross_aa", items=["top.op", "top.aa"]),
    CoverCross("top.op_cross_aa_bb", items=["top.op", "top.aa", "top.bb"]),
)


def sample_func(item):
    return item


sample_alu_coverage = alu_cov_obj(sample_func)


class AluCoverage(uvm_subscriber):
    """Coverage collector: collects coverage data for ALU operations and operand combinations"""

    def write(self, item):
        sample_alu_coverage(item)

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
            total_bins = 0
            covered_bins = 0
            for cover_point in coverage_db:
                cp_name = cover_point
                cp_size = coverage_db[cover_point].size
                cp_coverage = coverage_db[cover_point].coverage
                cp_detailed_coverage = coverage_db[cover_point].detailed_coverage

                total_bins += cp_size
                covered_bins += cp_coverage

                percentage = (cp_coverage / cp_size * 100) if cp_size > 0 else 0
                print(f"{cp_name:30} : {percentage:6.2f}% ({cp_coverage}/{cp_size})")

                if hasattr(coverage_db[cover_point], "bins") and len(
                    coverage_db[cover_point].bins
                ) < 20:
                    for bin_name, bin_hit in cp_detailed_coverage.items():
                        status = "HIT" if bin_hit > 0 else "MISS"
                        print(f"  {str(bin_name):25} : {status:4} (hits: {bin_hit})")

            print("-" * 60)
            overall_percentage = (covered_bins / total_bins * 100) if total_bins > 0 else 0
            print(
                f"{'OVERALL COVERAGE':30} : "
                f"{overall_percentage:6.2f}% ({covered_bins}/{total_bins})"
            )

        except Exception as e:
            print(f"Error accessing coverage: {e}")
            print("Attempting alternative method...")

        print("=" * 60 + "\n")
