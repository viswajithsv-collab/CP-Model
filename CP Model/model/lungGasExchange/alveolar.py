import numpy as np

def alveolarO2(VA, FA_O2_old, V_dot, FD_O2, VA_dot, K, Qpa, sh, Cpp_O2, Cv_O2, Vpp, dCpp_O2_dt, phase, dt):
    """Alveolar O2 balance (A44) with respiratory phase"""

    if phase == 1:  # Inspiration
        term1 = VA_dot * (FD_O2 - FA_O2_old)
    else:  # Expiration
        term1 = VA_dot * (FD_O2 - FA_O2_old)  # Both directions for alveolar

    term2 = K * (Qpa * (1 - sh) * (Cpp_O2 - Cv_O2) + Vpp * dCpp_O2_dt)
    dFA_O2 = (term1 - term2) / VA
    FA_O2_new = FA_O2_old + dFA_O2 * dt
    return FA_O2_new, dFA_O2


def alveolarCO2(VA, FA_CO2_old, V_dot, FD_CO2, VA_dot, K, Qpa, sh, Cpp_CO2, Cv_CO2, Vpp, dCpp_CO2_dt, phase, dt):
    """Alveolar CO2 balance (A45) with respiratory phase"""

    if phase == 1:  # Inspiration
        term1 = VA_dot * (FD_CO2 - FA_CO2_old)
    else:  # Expiration
        term1 = VA_dot * (FD_CO2 - FA_CO2_old)  # Both directions for alveolar

    term2 = K * (Qpa * (1 - sh) * (Cpp_CO2 - Cv_CO2) + Vpp * dCpp_CO2_dt)
    dFA_CO2 = (term1 - term2) / VA
    FA_CO2_new = FA_CO2_old + dFA_CO2 * dt
    return FA_CO2_new, dFA_CO2