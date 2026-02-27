# TinyALU Verification (cocotb + pyuvm)

## Prerequisites
- Python virtual environment with `cocotb` and `pyuvm` installed
- Verilator installed and available in `PATH`

## 1. Activate environment
```bash
source ~/cocotb-env/bin/activate
```

## 2. RTL lint check (optional but recommended)
```bash
verilator --lint-only --Wall --top tinyalu ./hdl/*.sv
```

## 3. Run simulation
```bash
cd tests
make clean
make SIM=verilator WAVES=1
```

## 4. Notes
- `SIM=verilator`: use Verilator as simulator backend.
- `WAVES=1`: enable waveform dump for debug.
- Test entry: `tests/test_tinyalu.py` (`run_test("AluTest")`).



