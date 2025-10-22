def volume(C, P, Vu):
    """Volume calculation (A37-A40)"""
    V = C * P + Vu
    return V

def calculateVuA(FRC, CA, P_pl_EE, V_l_EE, V_t_EE, V_b_EE):
    """
    Calculate alveolar unstressed volume from FRC (Equation 6)
    Vu,A = FRC + CA * Ppl,EE - Vl,EE - Vt,EE - Vb,EE
    """
    Vu_A = FRC + CA * P_pl_EE - V_l_EE - V_t_EE - V_b_EE
    return Vu_A

def deadSpace(Vl, Vtr, Vb):
    """Dead space volume (A41)"""
    VD = Vl + Vtr + Vb
    return VD