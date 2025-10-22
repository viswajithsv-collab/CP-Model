def coronaryO2(VT_hp, Vhp, Chp_O2_old, Qhp_in, Ca_O2, MO2_hp, dt):
    """Coronary O2 exchange (A57)"""
    dChp_O2 = (Qhp_in * (Ca_O2 - Chp_O2_old) - MO2_hp) / (VT_hp + Vhp)
    Chp_O2_new = Chp_O2_old + dChp_O2 * dt
    return Chp_O2_new, dChp_O2

def coronaryCO2(VT_hp, Vhp, Chp_CO2_old, Qhp_in, Ca_CO2, MCO2_hp, dt):
    """Coronary CO2 exchange (A58)"""
    dChp_CO2 = (Qhp_in * (Ca_CO2 - Chp_CO2_old) + MCO2_hp) / (VT_hp + Vhp)
    Chp_CO2_new = Chp_CO2_old + dChp_CO2 * dt
    return Chp_CO2_new, dChp_CO2