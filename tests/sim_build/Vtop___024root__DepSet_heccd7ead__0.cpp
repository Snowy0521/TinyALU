// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"
#include "Vtop___024root.h"

void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf);

void Vtop___024root___eval_ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VicoTriggered.word(0U))) {
        Vtop___024root___ico_sequent__TOP__0(vlSelf);
    }
}

VL_INLINE_OPT void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ico_sequent__TOP__0\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.tinyalu__DOT__start = vlSelfRef.start;
    vlSelfRef.tinyalu__DOT__result_mult = vlSelfRef.tinyalu__DOT__u_mult__DOT__result;
    vlSelfRef.tinyalu__DOT__result_aax = vlSelfRef.tinyalu__DOT__u_aax__DOT__result;
    vlSelfRef.tinyalu__DOT__done_mult = vlSelfRef.tinyalu__DOT__u_mult__DOT__done_q;
    vlSelfRef.tinyalu__DOT__done_aax = vlSelfRef.tinyalu__DOT__u_aax__DOT__done_int;
    vlSelfRef.tinyalu__DOT__u_aax__DOT__done = vlSelfRef.tinyalu__DOT__u_aax__DOT__done_int;
    vlSelfRef.tinyalu__DOT__u_mult__DOT__done = vlSelfRef.tinyalu__DOT__u_mult__DOT__done_q;
    vlSelfRef.tinyalu__DOT__op = vlSelfRef.op;
    vlSelfRef.tinyalu__DOT__start_single = ((1U & (~ 
                                                   ((IData)(vlSelfRef.op) 
                                                    >> 2U))) 
                                            && (IData)(vlSelfRef.start));
    vlSelfRef.tinyalu__DOT__start_multi = ((1U & ((IData)(vlSelfRef.op) 
                                                  >> 2U)) 
                                           && ((1U 
                                                & ((IData)(vlSelfRef.op) 
                                                   >> 2U)) 
                                               && (IData)(vlSelfRef.start)));
    if ((4U & (IData)(vlSelfRef.op))) {
        vlSelfRef.done = (((IData)(vlSelfRef.op) >> 2U) 
                          & (IData)(vlSelfRef.tinyalu__DOT__u_mult__DOT__done_q));
        vlSelfRef.result = ((4U & (IData)(vlSelfRef.op))
                             ? (IData)(vlSelfRef.tinyalu__DOT__u_mult__DOT__result)
                             : 0U);
    } else {
        vlSelfRef.done = vlSelfRef.tinyalu__DOT__u_aax__DOT__done_int;
        vlSelfRef.result = vlSelfRef.tinyalu__DOT__u_aax__DOT__result;
    }
    vlSelfRef.tinyalu__DOT__clk = vlSelfRef.clk;
    vlSelfRef.tinyalu__DOT__rst_n = vlSelfRef.rst_n;
    vlSelfRef.tinyalu__DOT__A = vlSelfRef.A;
    vlSelfRef.tinyalu__DOT__B = vlSelfRef.B;
    vlSelfRef.tinyalu__DOT__u_aax__DOT__op = vlSelfRef.tinyalu__DOT__op;
    vlSelfRef.tinyalu__DOT__u_aax__DOT__start = vlSelfRef.tinyalu__DOT__start_single;
    vlSelfRef.tinyalu__DOT__u_mult__DOT__start = vlSelfRef.tinyalu__DOT__start_multi;
    vlSelfRef.tinyalu__DOT__done = vlSelfRef.done;
    vlSelfRef.tinyalu__DOT__result = vlSelfRef.result;
    vlSelfRef.tinyalu__DOT__u_aax__DOT__clk = vlSelfRef.tinyalu__DOT__clk;
    vlSelfRef.tinyalu__DOT__u_mult__DOT__clk = vlSelfRef.tinyalu__DOT__clk;
    vlSelfRef.tinyalu__DOT__u_aax__DOT__rst_n = vlSelfRef.tinyalu__DOT__rst_n;
    vlSelfRef.tinyalu__DOT__u_mult__DOT__rst_n = vlSelfRef.tinyalu__DOT__rst_n;
    vlSelfRef.tinyalu__DOT__u_aax__DOT__A = vlSelfRef.tinyalu__DOT__A;
    vlSelfRef.tinyalu__DOT__u_mult__DOT__A = vlSelfRef.tinyalu__DOT__A;
    vlSelfRef.tinyalu__DOT__u_aax__DOT__B = vlSelfRef.tinyalu__DOT__B;
    vlSelfRef.tinyalu__DOT__u_mult__DOT__B = vlSelfRef.tinyalu__DOT__B;
}

void Vtop___024root___eval_triggers__ico(Vtop___024root* vlSelf);

bool Vtop___024root___eval_phase__ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VicoExecute;
    // Body
    Vtop___024root___eval_triggers__ico(vlSelf);
    __VicoExecute = vlSelfRef.__VicoTriggered.any();
    if (__VicoExecute) {
        Vtop___024root___eval_ico(vlSelf);
    }
    return (__VicoExecute);
}

void Vtop___024root___eval_act(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_act\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

void Vtop___024root___nba_sequent__TOP__0(Vtop___024root* vlSelf);

void Vtop___024root___eval_nba(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_nba\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((3ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vtop___024root___nba_sequent__TOP__0(vlSelf);
    }
}

VL_INLINE_OPT void Vtop___024root___nba_sequent__TOP__0(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__0\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __Vdly__tinyalu__DOT__u_mult__DOT__done1;
    __Vdly__tinyalu__DOT__u_mult__DOT__done1 = 0;
    CData/*0:0*/ __Vdly__tinyalu__DOT__u_mult__DOT__done2;
    __Vdly__tinyalu__DOT__u_mult__DOT__done2 = 0;
    CData/*0:0*/ __Vdly__tinyalu__DOT__u_mult__DOT__done3;
    __Vdly__tinyalu__DOT__u_mult__DOT__done3 = 0;
    // Body
    __Vdly__tinyalu__DOT__u_mult__DOT__done1 = vlSelfRef.tinyalu__DOT__u_mult__DOT__done1;
    __Vdly__tinyalu__DOT__u_mult__DOT__done2 = vlSelfRef.tinyalu__DOT__u_mult__DOT__done2;
    __Vdly__tinyalu__DOT__u_mult__DOT__done3 = vlSelfRef.tinyalu__DOT__u_mult__DOT__done3;
    if (vlSelfRef.rst_n) {
        __Vdly__tinyalu__DOT__u_mult__DOT__done1 = 
            ((IData)(vlSelfRef.tinyalu__DOT__start_multi) 
             & (~ (IData)(vlSelfRef.tinyalu__DOT__u_mult__DOT__done_q)));
        __Vdly__tinyalu__DOT__u_mult__DOT__done2 = 
            ((IData)(vlSelfRef.tinyalu__DOT__u_mult__DOT__done1) 
             & (~ (IData)(vlSelfRef.tinyalu__DOT__u_mult__DOT__done_q)));
        __Vdly__tinyalu__DOT__u_mult__DOT__done3 = 
            ((IData)(vlSelfRef.tinyalu__DOT__u_mult__DOT__done2) 
             & (~ (IData)(vlSelfRef.tinyalu__DOT__u_mult__DOT__done_q)));
        vlSelfRef.tinyalu__DOT__u_mult__DOT__done_q 
            = ((IData)(vlSelfRef.tinyalu__DOT__u_mult__DOT__done3) 
               & (~ (IData)(vlSelfRef.tinyalu__DOT__u_mult__DOT__done_q)));
        vlSelfRef.tinyalu__DOT__u_aax__DOT__done_int = 0U;
        if (((IData)(vlSelfRef.tinyalu__DOT__start_single) 
             & (0U != (IData)(vlSelfRef.op)))) {
            vlSelfRef.tinyalu__DOT__u_aax__DOT__done_int = 1U;
            vlSelfRef.tinyalu__DOT__u_aax__DOT__result 
                = (0xffffU & ((1U == (3U & (IData)(vlSelfRef.op)))
                               ? ((IData)(vlSelfRef.A) 
                                  + (IData)(vlSelfRef.B))
                               : ((2U == (3U & (IData)(vlSelfRef.op)))
                                   ? ((IData)(vlSelfRef.A) 
                                      & (IData)(vlSelfRef.B))
                                   : ((3U == (3U & (IData)(vlSelfRef.op)))
                                       ? ((IData)(vlSelfRef.A) 
                                          ^ (IData)(vlSelfRef.B))
                                       : 0U))));
        }
        vlSelfRef.tinyalu__DOT__u_mult__DOT__result 
            = vlSelfRef.tinyalu__DOT__u_mult__DOT__mult2;
        vlSelfRef.tinyalu__DOT__u_mult__DOT__mult2 
            = vlSelfRef.tinyalu__DOT__u_mult__DOT__mult1;
        vlSelfRef.tinyalu__DOT__u_mult__DOT__mult1 
            = (0xffffU & ((IData)(vlSelfRef.tinyalu__DOT__u_mult__DOT__a_q) 
                          * (IData)(vlSelfRef.tinyalu__DOT__u_mult__DOT__b_q)));
        vlSelfRef.tinyalu__DOT__u_mult__DOT__a_q = vlSelfRef.A;
        vlSelfRef.tinyalu__DOT__u_mult__DOT__b_q = vlSelfRef.B;
    } else {
        __Vdly__tinyalu__DOT__u_mult__DOT__done1 = 0U;
        __Vdly__tinyalu__DOT__u_mult__DOT__done2 = 0U;
        __Vdly__tinyalu__DOT__u_mult__DOT__done3 = 0U;
        vlSelfRef.tinyalu__DOT__u_mult__DOT__done_q = 0U;
        vlSelfRef.tinyalu__DOT__u_aax__DOT__done_int = 0U;
        vlSelfRef.tinyalu__DOT__u_aax__DOT__result = 0U;
        vlSelfRef.tinyalu__DOT__u_mult__DOT__result = 0U;
        vlSelfRef.tinyalu__DOT__u_mult__DOT__mult2 = 0U;
        vlSelfRef.tinyalu__DOT__u_mult__DOT__mult1 = 0U;
        vlSelfRef.tinyalu__DOT__u_mult__DOT__a_q = 0U;
        vlSelfRef.tinyalu__DOT__u_mult__DOT__b_q = 0U;
    }
    vlSelfRef.tinyalu__DOT__u_mult__DOT__done1 = __Vdly__tinyalu__DOT__u_mult__DOT__done1;
    vlSelfRef.tinyalu__DOT__u_mult__DOT__done2 = __Vdly__tinyalu__DOT__u_mult__DOT__done2;
    vlSelfRef.tinyalu__DOT__u_mult__DOT__done3 = __Vdly__tinyalu__DOT__u_mult__DOT__done3;
    vlSelfRef.tinyalu__DOT__done_mult = vlSelfRef.tinyalu__DOT__u_mult__DOT__done_q;
    vlSelfRef.tinyalu__DOT__u_mult__DOT__done = vlSelfRef.tinyalu__DOT__u_mult__DOT__done_q;
    vlSelfRef.tinyalu__DOT__done_aax = vlSelfRef.tinyalu__DOT__u_aax__DOT__done_int;
    vlSelfRef.tinyalu__DOT__u_aax__DOT__done = vlSelfRef.tinyalu__DOT__u_aax__DOT__done_int;
    if ((4U & (IData)(vlSelfRef.op))) {
        vlSelfRef.done = (((IData)(vlSelfRef.op) >> 2U) 
                          & (IData)(vlSelfRef.tinyalu__DOT__u_mult__DOT__done_q));
        vlSelfRef.result = ((4U & (IData)(vlSelfRef.op))
                             ? (IData)(vlSelfRef.tinyalu__DOT__u_mult__DOT__result)
                             : 0U);
    } else {
        vlSelfRef.done = vlSelfRef.tinyalu__DOT__u_aax__DOT__done_int;
        vlSelfRef.result = vlSelfRef.tinyalu__DOT__u_aax__DOT__result;
    }
    vlSelfRef.tinyalu__DOT__result_aax = vlSelfRef.tinyalu__DOT__u_aax__DOT__result;
    vlSelfRef.tinyalu__DOT__result_mult = vlSelfRef.tinyalu__DOT__u_mult__DOT__result;
    vlSelfRef.tinyalu__DOT__done = vlSelfRef.done;
    vlSelfRef.tinyalu__DOT__result = vlSelfRef.result;
}

void Vtop___024root___eval_triggers__act(Vtop___024root* vlSelf);

bool Vtop___024root___eval_phase__act(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__act\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    VlTriggerVec<2> __VpreTriggered;
    CData/*0:0*/ __VactExecute;
    // Body
    Vtop___024root___eval_triggers__act(vlSelf);
    __VactExecute = vlSelfRef.__VactTriggered.any();
    if (__VactExecute) {
        __VpreTriggered.andNot(vlSelfRef.__VactTriggered, vlSelfRef.__VnbaTriggered);
        vlSelfRef.__VnbaTriggered.thisOr(vlSelfRef.__VactTriggered);
        Vtop___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool Vtop___024root___eval_phase__nba(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__nba\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = vlSelfRef.__VnbaTriggered.any();
    if (__VnbaExecute) {
        Vtop___024root___eval_nba(vlSelf);
        vlSelfRef.__VnbaTriggered.clear();
    }
    return (__VnbaExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(Vtop___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__nba(Vtop___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__act(Vtop___024root* vlSelf);
#endif  // VL_DEBUG

void Vtop___024root___eval(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    IData/*31:0*/ __VicoIterCount;
    CData/*0:0*/ __VicoContinue;
    IData/*31:0*/ __VnbaIterCount;
    CData/*0:0*/ __VnbaContinue;
    // Body
    __VicoIterCount = 0U;
    vlSelfRef.__VicoFirstIteration = 1U;
    __VicoContinue = 1U;
    while (__VicoContinue) {
        if (VL_UNLIKELY(((0x64U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__ico(vlSelf);
#endif
            VL_FATAL_MT("../hdl/tinyalu.sv", 2, "", "Input combinational region did not converge.");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        __VicoContinue = 0U;
        if (Vtop___024root___eval_phase__ico(vlSelf)) {
            __VicoContinue = 1U;
        }
        vlSelfRef.__VicoFirstIteration = 0U;
    }
    __VnbaIterCount = 0U;
    __VnbaContinue = 1U;
    while (__VnbaContinue) {
        if (VL_UNLIKELY(((0x64U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__nba(vlSelf);
#endif
            VL_FATAL_MT("../hdl/tinyalu.sv", 2, "", "NBA region did not converge.");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        __VnbaContinue = 0U;
        vlSelfRef.__VactIterCount = 0U;
        vlSelfRef.__VactContinue = 1U;
        while (vlSelfRef.__VactContinue) {
            if (VL_UNLIKELY(((0x64U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                Vtop___024root___dump_triggers__act(vlSelf);
#endif
                VL_FATAL_MT("../hdl/tinyalu.sv", 2, "", "Active region did not converge.");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactContinue = 0U;
            if (Vtop___024root___eval_phase__act(vlSelf)) {
                vlSelfRef.__VactContinue = 1U;
            }
        }
        if (Vtop___024root___eval_phase__nba(vlSelf)) {
            __VnbaContinue = 1U;
        }
    }
}

#ifdef VL_DEBUG
void Vtop___024root___eval_debug_assertions(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_debug_assertions\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.clk & 0xfeU)))) {
        Verilated::overWidthError("clk");}
    if (VL_UNLIKELY(((vlSelfRef.rst_n & 0xfeU)))) {
        Verilated::overWidthError("rst_n");}
    if (VL_UNLIKELY(((vlSelfRef.start & 0xfeU)))) {
        Verilated::overWidthError("start");}
    if (VL_UNLIKELY(((vlSelfRef.op & 0xf8U)))) {
        Verilated::overWidthError("op");}
}
#endif  // VL_DEBUG
