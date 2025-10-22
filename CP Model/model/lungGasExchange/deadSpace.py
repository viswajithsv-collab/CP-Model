import numpy as np

def deadSpaceO2(VD, FD_O2_old, V_dot, FI_O2, VA_dot, FA_O2, phase, dt):
    """Dead space O2 balance (A42) with respiratory phase"""

    if phase == 1:  # Inspiration
        term1 = V_dot * (FI_O2 - FD_O2_old)
        term2 = 0
    else:  # Expiration
        term1 = 0
        term2 = VA_dot * (FD_O2_old - FA_O2)

    dFD_O2 = (term1 + term2) / VD
    FD_O2_new = FD_O2_old + dFD_O2 * dt
    return FD_O2_new, dFD_O2


def deadSpaceCO2(VD, FD_CO2_old, V_dot, FI_CO2, VA_dot, FA_CO2, phase, dt):
    """Dead space CO2 balance (A43) with respiratory phase"""

    if phase == 1:  # Inspiration
        term1 = V_dot * (FI_CO2 - FD_CO2_old)
        term2 = 0
    else:  # Expiration
        term1 = 0
        term2 = VA_dot * (FD_CO2_old - FA_CO2)

    dFD_CO2 = (term1 + term2) / VD
    FD_CO2_new = FD_CO2_old + dFD_CO2 * dt
    return FD_CO2_new, dFD_CO2