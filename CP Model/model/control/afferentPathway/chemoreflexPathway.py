import numpy as np


def chemoreceptorStatic(Pa_O2, Pa_CO2, f_ac_max, f_ac_min, P_O2ac, k_ac, K_H, f, Pa_CO2n):
    """
    Static chemoreceptor response with O2-CO2 interaction
    wac(Pa_O2, Pa_CO2) = O2_response * CO2_response

    Args:
        Pa_O2: Arterial oxygen pressure (mmHg)
        Pa_CO2: Arterial CO2 pressure (mmHg)
        f_ac_max, f_ac_min: Upper and lower saturation (spikes/s)
        P_O2ac: Central point of O2 response (mmHg)
        k_ac: O2 slope parameter (mmHg)
        K_H: CO2 sensitivity parameter
        f: CO2 interaction parameter
        Pa_CO2n: Normal CO2 pressure (mmHg)
    """
    # O2 response (sigmoid)
    exp_term = np.exp((Pa_O2 - P_O2ac) / k_ac)
    O2_response = (f_ac_min + f_ac_max * exp_term) / (1 + exp_term)

    # Variable CO2 sensitivity based on O2 level
    if Pa_O2 > 80:
        K = K_H
    elif Pa_O2 > 40:
        K = K_H - 1.2 * ((Pa_O2 - 80) / 30)
    else:
        K = K_H - 1.6

    # CO2 response
    if Pa_CO2 > 0 and Pa_CO2n > 0:
        CO2_term = K * np.log(Pa_CO2 / Pa_CO2n) + f
    else:
        CO2_term = f

    # Multiplicative interaction
    wac = O2_response * CO2_term
    return max(0, wac)


def chemoreceptorDynamics(f_ac, Pa_O2, Pa_CO2, f_ac_max, f_ac_min, P_O2ac, k_ac, K_H, f, Pa_CO2n, tau_ac):
    """
    Peripheral chemoreceptor dynamics
    df_ac/dt = (1/τ_ac) * (-f_ac + wac)

    Args:
        f_ac: Current chemoreceptor activity (spikes/s)
        Pa_O2: Arterial oxygen pressure (mmHg)
        Pa_CO2: Arterial CO2 pressure (mmHg)
        [other parameters as above]
        tau_ac: Time constant (s)
    """
    wac = chemoreceptorStatic(Pa_O2, Pa_CO2, f_ac_max, f_ac_min, P_O2ac, k_ac, K_H, f, Pa_CO2n)
    df_ac_dt = (1 / tau_ac) * (-f_ac + wac)
    return df_ac_dt