import numpy as np

def o2Concentration(Csat_O2, Xpp_O2, h1):
    """O2 concentration (A46)"""
    Cpp_O2 = Csat_O2 * (Xpp_O2**(1/h1)) / (1 + (Xpp_O2**(1/h1)))
    return Cpp_O2

def o2SaturationVariable(Ppp_O2, beta1, Ppp_CO2, K1, alpha1):
    """O2 saturation variable (A47)"""
    Xpp_O2 = Ppp_O2 * (1 + beta1 * Ppp_CO2) / (K1 * (1 + alpha1 * Ppp_CO2))
    return Xpp_O2

def co2Concentration(Csat_CO2, Xpp_CO2, h2):
    """CO2 concentration (A48)"""
    Cpp_CO2 = Csat_CO2 * (Xpp_CO2**(1/h2)) / (1 + (Xpp_CO2**(1/h2)))
    return Cpp_CO2

def co2SaturationVariable(Ppp_CO2, beta2, Ppp_O2, K2, alpha2):
    """CO2 saturation variable (A49)"""
    Xpp_CO2 = Ppp_CO2 * (1 + beta2 * Ppp_O2) / (K2 * (1 + alpha2 * Ppp_O2))
    return Xpp_CO2