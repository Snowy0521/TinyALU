// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vtop__pch.h"
#include "Vtop.h"
#include "Vtop___024root.h"

// FUNCTIONS
Vtop__Syms::~Vtop__Syms()
{

    // Tear down scope hierarchy
    __Vhier.remove(0, &__Vscope_tinyalu);
    __Vhier.remove(&__Vscope_tinyalu, &__Vscope_tinyalu__u_aax);
    __Vhier.remove(&__Vscope_tinyalu, &__Vscope_tinyalu__u_mult);

}

Vtop__Syms::Vtop__Syms(VerilatedContext* contextp, const char* namep, Vtop* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
{
        // Check resources
        Verilated::stackCheck(31);
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscope_TOP.configure(this, name(), "TOP", "TOP", "<null>", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_tinyalu.configure(this, name(), "tinyalu", "tinyalu", "tinyalu", -9, VerilatedScope::SCOPE_MODULE);
    __Vscope_tinyalu__u_aax.configure(this, name(), "tinyalu.u_aax", "u_aax", "single_cycle", -9, VerilatedScope::SCOPE_MODULE);
    __Vscope_tinyalu__u_mult.configure(this, name(), "tinyalu.u_mult", "u_mult", "three_cycle", -9, VerilatedScope::SCOPE_MODULE);

    // Set up scope hierarchy
    __Vhier.add(0, &__Vscope_tinyalu);
    __Vhier.add(&__Vscope_tinyalu, &__Vscope_tinyalu__u_aax);
    __Vhier.add(&__Vscope_tinyalu, &__Vscope_tinyalu__u_mult);

    // Setup export functions
    for (int __Vfinal = 0; __Vfinal < 2; ++__Vfinal) {
        __Vscope_TOP.varInsert(__Vfinal,"A", &(TOP.A), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_TOP.varInsert(__Vfinal,"B", &(TOP.B), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_TOP.varInsert(__Vfinal,"clk", &(TOP.clk), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"done", &(TOP.done), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"op", &(TOP.op), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,1 ,2,0);
        __Vscope_TOP.varInsert(__Vfinal,"result", &(TOP.result), false, VLVT_UINT16,VLVD_OUT|VLVF_PUB_RW,0,1 ,15,0);
        __Vscope_TOP.varInsert(__Vfinal,"rst_n", &(TOP.rst_n), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"start", &(TOP.start), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu.varInsert(__Vfinal,"A", &(TOP.tinyalu__DOT__A), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_tinyalu.varInsert(__Vfinal,"B", &(TOP.tinyalu__DOT__B), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_tinyalu.varInsert(__Vfinal,"clk", &(TOP.tinyalu__DOT__clk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu.varInsert(__Vfinal,"done", &(TOP.tinyalu__DOT__done), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu.varInsert(__Vfinal,"done_aax", &(TOP.tinyalu__DOT__done_aax), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu.varInsert(__Vfinal,"done_mult", &(TOP.tinyalu__DOT__done_mult), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu.varInsert(__Vfinal,"op", &(TOP.tinyalu__DOT__op), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,2,0);
        __Vscope_tinyalu.varInsert(__Vfinal,"result", &(TOP.tinyalu__DOT__result), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RW,0,1 ,15,0);
        __Vscope_tinyalu.varInsert(__Vfinal,"result_aax", &(TOP.tinyalu__DOT__result_aax), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RW,0,1 ,15,0);
        __Vscope_tinyalu.varInsert(__Vfinal,"result_mult", &(TOP.tinyalu__DOT__result_mult), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RW,0,1 ,15,0);
        __Vscope_tinyalu.varInsert(__Vfinal,"rst_n", &(TOP.tinyalu__DOT__rst_n), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu.varInsert(__Vfinal,"start", &(TOP.tinyalu__DOT__start), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu.varInsert(__Vfinal,"start_multi", &(TOP.tinyalu__DOT__start_multi), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu.varInsert(__Vfinal,"start_single", &(TOP.tinyalu__DOT__start_single), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu__u_aax.varInsert(__Vfinal,"A", &(TOP.tinyalu__DOT__u_aax__DOT__A), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_tinyalu__u_aax.varInsert(__Vfinal,"B", &(TOP.tinyalu__DOT__u_aax__DOT__B), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_tinyalu__u_aax.varInsert(__Vfinal,"clk", &(TOP.tinyalu__DOT__u_aax__DOT__clk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu__u_aax.varInsert(__Vfinal,"done", &(TOP.tinyalu__DOT__u_aax__DOT__done), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu__u_aax.varInsert(__Vfinal,"done_int", &(TOP.tinyalu__DOT__u_aax__DOT__done_int), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu__u_aax.varInsert(__Vfinal,"op", &(TOP.tinyalu__DOT__u_aax__DOT__op), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,2,0);
        __Vscope_tinyalu__u_aax.varInsert(__Vfinal,"result", &(TOP.tinyalu__DOT__u_aax__DOT__result), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RW,0,1 ,15,0);
        __Vscope_tinyalu__u_aax.varInsert(__Vfinal,"rst_n", &(TOP.tinyalu__DOT__u_aax__DOT__rst_n), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu__u_aax.varInsert(__Vfinal,"start", &(TOP.tinyalu__DOT__u_aax__DOT__start), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu__u_mult.varInsert(__Vfinal,"A", &(TOP.tinyalu__DOT__u_mult__DOT__A), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_tinyalu__u_mult.varInsert(__Vfinal,"B", &(TOP.tinyalu__DOT__u_mult__DOT__B), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_tinyalu__u_mult.varInsert(__Vfinal,"a_q", &(TOP.tinyalu__DOT__u_mult__DOT__a_q), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_tinyalu__u_mult.varInsert(__Vfinal,"b_q", &(TOP.tinyalu__DOT__u_mult__DOT__b_q), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_tinyalu__u_mult.varInsert(__Vfinal,"clk", &(TOP.tinyalu__DOT__u_mult__DOT__clk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu__u_mult.varInsert(__Vfinal,"done", &(TOP.tinyalu__DOT__u_mult__DOT__done), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu__u_mult.varInsert(__Vfinal,"done1", &(TOP.tinyalu__DOT__u_mult__DOT__done1), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu__u_mult.varInsert(__Vfinal,"done2", &(TOP.tinyalu__DOT__u_mult__DOT__done2), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu__u_mult.varInsert(__Vfinal,"done3", &(TOP.tinyalu__DOT__u_mult__DOT__done3), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu__u_mult.varInsert(__Vfinal,"done_q", &(TOP.tinyalu__DOT__u_mult__DOT__done_q), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu__u_mult.varInsert(__Vfinal,"mult1", &(TOP.tinyalu__DOT__u_mult__DOT__mult1), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RW,0,1 ,15,0);
        __Vscope_tinyalu__u_mult.varInsert(__Vfinal,"mult2", &(TOP.tinyalu__DOT__u_mult__DOT__mult2), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RW,0,1 ,15,0);
        __Vscope_tinyalu__u_mult.varInsert(__Vfinal,"result", &(TOP.tinyalu__DOT__u_mult__DOT__result), false, VLVT_UINT16,VLVD_NODIR|VLVF_PUB_RW,0,1 ,15,0);
        __Vscope_tinyalu__u_mult.varInsert(__Vfinal,"rst_n", &(TOP.tinyalu__DOT__u_mult__DOT__rst_n), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_tinyalu__u_mult.varInsert(__Vfinal,"start", &(TOP.tinyalu__DOT__u_mult__DOT__start), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
    }
}
