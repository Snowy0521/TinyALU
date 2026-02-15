// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"
#include "Vtop___024root.h"

VL_ATTR_COLD void Vtop___024root___eval_static(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_static\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__rst_n__0 = vlSelfRef.rst_n;
}

VL_ATTR_COLD void Vtop___024root___eval_initial(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_initial\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vtop___024root___eval_final(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_final\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__stl(Vtop___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vtop___024root___eval_phase__stl(Vtop___024root* vlSelf);

VL_ATTR_COLD void Vtop___024root___eval_settle(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_settle\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    IData/*31:0*/ __VstlIterCount;
    CData/*0:0*/ __VstlContinue;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    __VstlContinue = 1U;
    while (__VstlContinue) {
        if (VL_UNLIKELY(((0x64U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__stl(vlSelf);
#endif
            VL_FATAL_MT("../hdl/tinyalu.sv", 2, "", "Settle region did not converge.");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        __VstlContinue = 0U;
        if (Vtop___024root___eval_phase__stl(vlSelf)) {
            __VstlContinue = 1U;
        }
        vlSelfRef.__VstlFirstIteration = 0U;
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VstlTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VstlTriggered.word(0U))) {
        VL_DBG_MSGF("         'stl' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf);

VL_ATTR_COLD void Vtop___024root___eval_stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered.word(0U))) {
        Vtop___024root___ico_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD void Vtop___024root___eval_triggers__stl(Vtop___024root* vlSelf);

VL_ATTR_COLD bool Vtop___024root___eval_phase__stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VstlExecute;
    // Body
    Vtop___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = vlSelfRef.__VstlTriggered.any();
    if (__VstlExecute) {
        Vtop___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VicoTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VicoTriggered.word(0U))) {
        VL_DBG_MSGF("         'ico' region trigger index 0 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__act(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__act\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VactTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 0 is active: @(posedge clk)\n");
    }
    if ((2ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 1 is active: @(negedge rst_n)\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__nba(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__nba\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VnbaTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 0 is active: @(posedge clk)\n");
    }
    if ((2ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 1 is active: @(negedge rst_n)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtop___024root___ctor_var_reset(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ctor_var_reset\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->name());
    vlSelf->clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16707436170211756652ull);
    vlSelf->rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1638864771569018232ull);
    vlSelf->start = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9867861323841650631ull);
    vlSelf->op = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3630531923276091163ull);
    vlSelf->A = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3969090544990846983ull);
    vlSelf->B = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 149303876845869574ull);
    vlSelf->done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10296494685231209730ull);
    vlSelf->result = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16664408842984530663ull);
    vlSelf->tinyalu__DOT__clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2333813654495583076ull);
    vlSelf->tinyalu__DOT__rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8580988242205505759ull);
    vlSelf->tinyalu__DOT__start = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6404035979388233304ull);
    vlSelf->tinyalu__DOT__op = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1801727025132543593ull);
    vlSelf->tinyalu__DOT__A = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4576434831524734945ull);
    vlSelf->tinyalu__DOT__B = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12344553233789553882ull);
    vlSelf->tinyalu__DOT__done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6551589126182515052ull);
    vlSelf->tinyalu__DOT__result = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13601350846593169604ull);
    vlSelf->tinyalu__DOT__start_single = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13027682862172100441ull);
    vlSelf->tinyalu__DOT__start_multi = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15614838314725598532ull);
    vlSelf->tinyalu__DOT__done_aax = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4241762260350492552ull);
    vlSelf->tinyalu__DOT__done_mult = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5491809620746966935ull);
    vlSelf->tinyalu__DOT__result_aax = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9612854248408187370ull);
    vlSelf->tinyalu__DOT__result_mult = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14288632963061214037ull);
    vlSelf->tinyalu__DOT__u_aax__DOT__clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6351399245127631032ull);
    vlSelf->tinyalu__DOT__u_aax__DOT__rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11045293741727397863ull);
    vlSelf->tinyalu__DOT__u_aax__DOT__start = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 80365892802904510ull);
    vlSelf->tinyalu__DOT__u_aax__DOT__op = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17921774226171185528ull);
    vlSelf->tinyalu__DOT__u_aax__DOT__A = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8676410063100781359ull);
    vlSelf->tinyalu__DOT__u_aax__DOT__B = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7971929533788002131ull);
    vlSelf->tinyalu__DOT__u_aax__DOT__done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15063224840383545031ull);
    vlSelf->tinyalu__DOT__u_aax__DOT__result = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14649026752562586482ull);
    vlSelf->tinyalu__DOT__u_aax__DOT__done_int = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7652916004394610399ull);
    vlSelf->tinyalu__DOT__u_mult__DOT__clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9259327283706295664ull);
    vlSelf->tinyalu__DOT__u_mult__DOT__rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1346967470547246903ull);
    vlSelf->tinyalu__DOT__u_mult__DOT__start = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9555836219051186865ull);
    vlSelf->tinyalu__DOT__u_mult__DOT__A = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16736655305189482155ull);
    vlSelf->tinyalu__DOT__u_mult__DOT__B = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1797479040939948851ull);
    vlSelf->tinyalu__DOT__u_mult__DOT__done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4304320891685290530ull);
    vlSelf->tinyalu__DOT__u_mult__DOT__result = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13064294776916470635ull);
    vlSelf->tinyalu__DOT__u_mult__DOT__a_q = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16444575511937168895ull);
    vlSelf->tinyalu__DOT__u_mult__DOT__b_q = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15741086039431827033ull);
    vlSelf->tinyalu__DOT__u_mult__DOT__mult1 = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14589867580409326431ull);
    vlSelf->tinyalu__DOT__u_mult__DOT__mult2 = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14992047949854328613ull);
    vlSelf->tinyalu__DOT__u_mult__DOT__done1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17030551824504128128ull);
    vlSelf->tinyalu__DOT__u_mult__DOT__done2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12119715299824519197ull);
    vlSelf->tinyalu__DOT__u_mult__DOT__done3 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12387147740739748217ull);
    vlSelf->tinyalu__DOT__u_mult__DOT__done_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6662739232155471482ull);
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9526919608049418986ull);
    vlSelf->__Vtrigprevexpr___TOP__rst_n__0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14803524876191471008ull);
}
