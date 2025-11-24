def coronaryVenousO2(Vhv, Chv_O2_old, Qhp, Chp_O2, dt):
    """Coronary venous O2 transport (A67)"""
    dChv_O2 = Qhp * (Chp_O2 - Chv_O2_old) / Vhv
    Chv_O2_new = Chv_O2_old + dChv_O2 * dt
    return Chv_O2_new, dChv_O2

def coronaryVenousCO2(Vhv, Chv_CO2_old, Qhp, Chp_CO2, dt):
    """Coronary venous CO2 transport (A68)"""
    dChv_CO2 = Qhp * (Chp_CO2 - Chv_CO2_old) / Vhv
    Chv_CO2_new = Chv_CO2_old + dChv_CO2 * dt
    return Chv_CO2_new, dChv_CO2