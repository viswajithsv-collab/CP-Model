def extrasplanchnicVenousO2(Vev, Cev_O2_old, Qep, Cep_O2, dt):
    """Extrasplanchnic venous O2 transport (A73)"""
    dCev_O2 = Qep * (Cep_O2 - Cev_O2_old) / Vev
    Cev_O2_new = Cev_O2_old + dCev_O2 * dt
    return Cev_O2_new, dCev_O2

def extrasplanchnicVenousCO2(Vev, Cev_CO2_old, Qep, Cep_CO2, dt):
    """Extrasplanchnic venous CO2 transport (A74)"""
    dCev_CO2 = Qep * (Cep_CO2 - Cev_CO2_old) / Vev
    Cev_CO2_new = Cev_CO2_old + dCev_CO2 * dt
    return Cev_CO2_new, dCev_CO2