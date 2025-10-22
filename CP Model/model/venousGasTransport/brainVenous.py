def brainVenousO2(Vbv, Cbv_O2_old, Qbp, Cbp_O2, dt):
    """Brain venous O2 transport (A69)"""
    dCbv_O2 = Qbp * (Cbp_O2 - Cbv_O2_old) / Vbv
    Cbv_O2_new = Cbv_O2_old + dCbv_O2 * dt
    return Cbv_O2_new, dCbv_O2

def brainVenousCO2(Vbv, Cbv_CO2_old, Qbp, Cbp_CO2, dt):
    """Brain venous CO2 transport (A70)"""
    dCbv_CO2 = Qbp * (Cbp_CO2 - Cbv_CO2_old) / Vbv
    Cbv_CO2_new = Cbv_CO2_old + dCbv_CO2 * dt
    return Cbv_CO2_new, dCbv_CO2