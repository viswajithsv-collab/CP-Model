def extrasplanchnicO2(VT_ep, Vep, Cep_O2_old, Qep_in, Ca_O2, MO2_ep, dt):
    """Extrasplanchnic O2 exchange (A63)"""
    dCep_O2 = (Qep_in * (Ca_O2 - Cep_O2_old) - MO2_ep) / (VT_ep + Vep)
    Cep_O2_new = Cep_O2_old + dCep_O2 * dt
    return Cep_O2_new, dCep_O2

def extrasplanchnicCO2(VT_ep, Vep, Cep_CO2_old, Qep_in, Ca_CO2, MCO2_ep, dt):
    """Extrasplanchnic CO2 exchange (A64)"""
    dCep_CO2 = (Qep_in * (Ca_CO2 - Cep_CO2_old) + MCO2_ep) / (VT_ep + Vep)
    Cep_CO2_new = Cep_CO2_old + dCep_CO2 * dt
    return Cep_CO2_new, dCep_CO2