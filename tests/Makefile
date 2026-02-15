SIM ?= verilator
TOPLEVEL = tinyalu
TOPLEVEL_LANG = verilog
COCOTB_TEST_MODULES = test_tinyalu

VERILOG_SOURCES += ../hdl/tinyalu.sv ../hdl/single_cycle.sv ../hdl/three_cycle.sv

VERILATOR_ARGS += --trace --trace-structs -Wno-WIDTH -Wno-UNUSED

COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

include $(shell cocotb-config --makefiles)/Makefile.sim