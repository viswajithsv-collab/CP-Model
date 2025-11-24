def splanchnicO2(VT_sp, Vsp, Csp_O2_old, Qsp_in, Ca_O2, MO2_sp, dt):
    """Splanchnic O2 exchange (A65)"""
    dCsp_O2 = (Qsp_in * (Ca_O2 - Csp_O2_old) - MO2_sp) / (VT_sp + Vsp)
    Csp_O2_new = Csp_O2_old + dCsp_O2 * dt
    return Csp_O2_new, dCsp_O2

def splanchnicCO2(VT_sp, Vsp, Csp_CO2_old, Qsp_in, Ca_CO2, MCO2_sp, dt):
    """Splanchnic CO2 exchange (A66)"""
    dCsp_CO2 = (Qsp_in * (Ca_CO2 - Csp_CO2_old) + MCO2_sp) / (VT_sp + Vsp)
    Csp_CO2_new = Csp_CO2_old + dCsp_CO2 * dt
    return Csp_CO2_new, dCsp_CO2