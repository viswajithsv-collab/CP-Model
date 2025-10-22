def activeMuscleO2(VT_amp, Vamp, Camp_O2_old, Qamp_in, Ca_O2, MO2_amp, dt):
    """Active muscle O2 exchange (A61)"""
    dCamp_O2 = (Qamp_in * (Ca_O2 - Camp_O2_old) - MO2_amp) / (VT_amp + Vamp)
    Camp_O2_new = Camp_O2_old + dCamp_O2 * dt
    return Camp_O2_new, dCamp_O2

def activeMuscleCO2(VT_amp, Vamp, Camp_CO2_old, Qamp_in, Ca_CO2, MCO2_amp, dt):
    """Active muscle CO2 exchange (A62)"""
    dCamp_CO2 = (Qamp_in * (Ca_CO2 - Camp_CO2_old) + MCO2_amp) / (VT_amp + Vamp)
    Camp_CO2_new = Camp_CO2_old + dCamp_CO2 * dt
    return Camp_CO2_new, dCamp_CO2