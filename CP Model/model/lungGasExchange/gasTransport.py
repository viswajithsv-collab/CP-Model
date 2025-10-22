def arterialGasMixing(Qpp, Cpp_O2, Qps, Cv_O2):
    """Arterial O2 mixing - shunt + gas exchange (A54)"""
    Ca_O2 = (Qpp * Cpp_O2 + Qps * Cv_O2) / (Qpp + Qps)
    return Ca_O2

def arterialCO2Mixing(Qpp, Cpp_CO2, Qps, Cv_CO2):
    """Arterial CO2 mixing - shunt + gas exchange (A55)"""
    Ca_CO2 = (Qpp * Cpp_CO2 + Qps * Cv_CO2) / (Qpp + Qps)
    return Ca_CO2

def arterialO2Saturation(Ca_O2, Pa_O2, Hgb):
    """Arterial O2 saturation percentage (A56)"""
    Sa_O2_percent = ((Ca_O2 - Pa_O2 * 0.003/100) / (Hgb * 1.34)) * 100
    return Sa_O2_percent