def restingMuscleO2(VT_rmp, Vrmp, Crmp_O2_old, Qrmp_in, Ca_O2, MO2_rmp, dt):
    """Resting muscle O2 exchange (A61 variant)"""
    dCrmp_O2 = (Qrmp_in * (Ca_O2 - Crmp_O2_old) - MO2_rmp) / (VT_rmp + Vrmp)
    Crmp_O2_new = Crmp_O2_old + dCrmp_O2 * dt
    return Crmp_O2_new, dCrmp_O2

def restingMuscleCO2(VT_rmp, Vrmp, Crmp_CO2_old, Qrmp_in, Ca_CO2, MCO2_rmp, dt):
    """Resting muscle CO2 exchange (A62 variant)"""
    dCrmp_CO2 = (Qrmp_in * (Ca_CO2 - Crmp_CO2_old) + MCO2_rmp) / (VT_rmp + Vrmp)
    Crmp_CO2_new = Crmp_CO2_old + dCrmp_CO2 * dt
    return Crmp_CO2_new, dCrmp_CO2