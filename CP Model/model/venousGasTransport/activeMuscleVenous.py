def activeMuscleVenousO2(Vamv, Camv_O2_old, Qamp, Camp_O2, dt):
    """Active muscle venous O2 transport (A71)"""
    dCamv_O2 = Qamp * (Camp_O2 - Camv_O2_old) / Vamv
    Camv_O2_new = Camv_O2_old + dCamv_O2 * dt
    return Camv_O2_new, dCamv_O2

def activeMuscleVenousCO2(Vamv, Camv_CO2_old, Qamp, Camp_CO2, dt):
    """Active muscle venous CO2 transport (A72)"""
    dCamv_CO2 = Qamp * (Camp_CO2 - Camv_CO2_old) / Vamv
    Camv_CO2_new = Camv_CO2_old + dCamv_CO2 * dt
    return Camv_CO2_new, dCamv_CO2