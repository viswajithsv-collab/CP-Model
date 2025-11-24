def alveolarPressures(FA_O2, FA_CO2, Patm, Pws):
    """Convert alveolar fractions to pressures (A52, A53)"""
    PA_O2 = FA_O2 * (Patm - Pws)
    PA_CO2 = FA_CO2 * (Patm - Pws)
    return PA_O2, PA_CO2

def equilibriumPressures(PA_O2, PA_CO2):
    """Equilibrium between alveoli and capillaries (A50, A51)"""
    Ppp_O2 = PA_O2
    Ppp_CO2 = PA_CO2
    return Ppp_O2, Ppp_CO2