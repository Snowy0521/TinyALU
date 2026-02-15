// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtop.h for the primary calling header

#ifndef VERILATED_VTOP___024ROOT_H_
#define VERILATED_VTOP___024ROOT_H_  // guard

#include "verilated.h"


class Vtop__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtop___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(clk,0,0);
    VL_IN8(rst_n,0,0);
    VL_IN8(start,0,0);
    VL_IN8(op,2,0);
    VL_IN8(A,7,0);
    VL_IN8(B,7,0);
    VL_OUT8(done,0,0);
    CData/*0:0*/ tinyalu__DOT__clk;
    CData/*0:0*/ tinyalu__DOT__rst_n;
    CData/*0:0*/ tinyalu__DOT__start;
    CData/*2:0*/ tinyalu__DOT__op;
    CData/*7:0*/ tinyalu__DOT__A;
    CData/*7:0*/ tinyalu__DOT__B;
    CData/*0:0*/ tinyalu__DOT__done;
    CData/*0:0*/ tinyalu__DOT__start_single;
    CData/*0:0*/ tinyalu__DOT__start_multi;
    CData/*0:0*/ tinyalu__DOT__done_aax;
    CData/*0:0*/ tinyalu__DOT__done_mult;
    CData/*0:0*/ tinyalu__DOT__u_aax__DOT__clk;
    CData/*0:0*/ tinyalu__DOT__u_aax__DOT__rst_n;
    CData/*0:0*/ tinyalu__DOT__u_aax__DOT__start;
    CData/*2:0*/ tinyalu__DOT__u_aax__DOT__op;
    CData/*7:0*/ tinyalu__DOT__u_aax__DOT__A;
    CData/*7:0*/ tinyalu__DOT__u_aax__DOT__B;
    CData/*0:0*/ tinyalu__DOT__u_aax__DOT__done;
    CData/*0:0*/ tinyalu__DOT__u_aax__DOT__done_int;
    CData/*0:0*/ tinyalu__DOT__u_mult__DOT__clk;
    CData/*0:0*/ tinyalu__DOT__u_mult__DOT__rst_n;
    CData/*0:0*/ tinyalu__DOT__u_mult__DOT__start;
    CData/*7:0*/ tinyalu__DOT__u_mult__DOT__A;
    CData/*7:0*/ tinyalu__DOT__u_mult__DOT__B;
    CData/*0:0*/ tinyalu__DOT__u_mult__DOT__done;
    CData/*7:0*/ tinyalu__DOT__u_mult__DOT__a_q;
    CData/*7:0*/ tinyalu__DOT__u_mult__DOT__b_q;
    CData/*0:0*/ tinyalu__DOT__u_mult__DOT__done1;
    CData/*0:0*/ tinyalu__DOT__u_mult__DOT__done2;
    CData/*0:0*/ tinyalu__DOT__u_mult__DOT__done3;
    CData/*0:0*/ tinyalu__DOT__u_mult__DOT__done_q;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VicoFirstIteration;
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__rst_n__0;
    CData/*0:0*/ __VactContinue;
    VL_OUT16(result,15,0);
    SData/*15:0*/ tinyalu__DOT__result;
    SData/*15:0*/ tinyalu__DOT__result_aax;
    SData/*15:0*/ tinyalu__DOT__result_mult;
    SData/*15:0*/ tinyalu__DOT__u_aax__DOT__result;
    SData/*15:0*/ tinyalu__DOT__u_mult__DOT__result;
    SData/*15:0*/ tinyalu__DOT__u_mult__DOT__mult1;
    SData/*15:0*/ tinyalu__DOT__u_mult__DOT__mult2;
    IData/*31:0*/ __VactIterCount;
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<1> __VicoTriggered;
    VlTriggerVec<2> __VactTriggered;
    VlTriggerVec<2> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vtop__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vtop___024root(Vtop__Syms* symsp, const char* v__name);
    ~Vtop___024root();
    VL_UNCOPYABLE(Vtop___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
