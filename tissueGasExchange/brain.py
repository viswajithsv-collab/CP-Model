def brainO2(VT_bp, Vbp, Cbp_O2_old, Qbp_in, Ca_O2, MO2_bp, dt):
    """Brain O2 exchange (A59)"""
    dCbp_O2 = (Qbp_in * (Ca_O2 - Cbp_O2_old) - MO2_bp) / (VT_bp + Vbp)
    Cbp_O2_new = Cbp_O2_old + dCbp_O2 * dt
    return Cbp_O2_new, dCbp_O2

def brainCO2(VT_bp, Vbp, Cbp_CO2_old, Qbp_in, Ca_CO2, MCO2_bp, dt):
    """Brain CO2 exchange (A60)"""
    dCbp_CO2 = (Qbp_in * (Ca_CO2 - Cbp_CO2_old) + MCO2_bp) / (VT_bp + Vbp)
    Cbp_CO2_new = Cbp_CO2_old + dCbp_CO2 * dt
    return Cbp_CO2_new, dCbp_CO2