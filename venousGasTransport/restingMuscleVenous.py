def restingMuscleVenousO2(Vrmv, Crmv_O2_old, Qrmp, Crmp_O2, dt):
    """Resting muscle venous O2 transport (A71 variant)"""
    dCrmv_O2 = Qrmp * (Crmp_O2 - Crmv_O2_old) / Vrmv
    Crmv_O2_new = Crmv_O2_old + dCrmv_O2 * dt
    return Crmv_O2_new, dCrmv_O2

def restingMuscleVenousCO2(Vrmv, Crmv_CO2_old, Qrmp, Crmp_CO2, dt):
    """Resting muscle venous CO2 transport (A72 variant)"""
    dCrmv_CO2 = Qrmp * (Crmp_CO2 - Crmv_CO2_old) / Vrmv
    Crmv_CO2_new = Crmv_CO2_old + dCrmv_CO2 * dt
    return Crmv_CO2_new, dCrmv_CO2