import cocotb
from cocotb.clock import Clock
from pyuvm import ConfigDB, uvm_root

from config import AGENT_CONFIGS
from tinyalu_bfm import TinyAluBfm
from uvm_components import AluTest


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

    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start()) # background continuous clock generation
    print("Clock started (10ns period, 100MHz)")

    bfm = TinyAluBfm(dut)
    await bfm.reset()
    print("DUT reset completed")

    for agent_cfg in AGENT_CONFIGS:
        ConfigDB().set(None, "*", agent_cfg.bfm_key, bfm)
    print("BFM handle(s) stored in ConfigDB for configured agent key(s)")

    _ = AluTest
    
    print("\n" + "Starting UVM test..." + "\n")
    await uvm_root().run_test("AluTest", keep_set={ConfigDB})

    print("\n" + "=" * 70)
    print(" " * 25 + "TEST COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    print(__doc__)
    print("\nRun with:")
    print("  make clean")
    print("  make SIM=verilator WAVE=1")
