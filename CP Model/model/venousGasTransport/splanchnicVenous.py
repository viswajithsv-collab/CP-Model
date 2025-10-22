def splanchnicVenousO2(Vsv, Csv_O2_old, Qsp, Csp_O2, dt):
    """Splanchnic venous O2 transport (A75)"""
    dCsv_O2 = Qsp * (Csp_O2 - Csv_O2_old) / Vsv
    Csv_O2_new = Csv_O2_old + dCsv_O2 * dt
    return Csv_O2_new, dCsv_O2

def splanchnicVenousCO2(Vsv, Csv_CO2_old, Qsp, Csp_CO2, dt):
    """Splanchnic venous CO2 transport (A76)"""
    dCsv_CO2 = Qsp * (Csp_CO2 - Csv_CO2_old) / Vsv
    Csv_CO2_new = Csv_CO2_old + dCsv_CO2 * dt
    return Csv_CO2_new, dCsv_CO2