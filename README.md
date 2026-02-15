1. activate cocotb-env
source ~/cocotb-env/bin/activate

2. linting check 
verilator --lint-only --Wall --top tinyalu ./hdl/*sv

3. clean cache
cd tests
make clean

4. run
make SIM=verilator WAVES=1




