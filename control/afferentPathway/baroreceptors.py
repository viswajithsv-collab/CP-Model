import numpy as np


def linearDerivativeFilter(P_b, dP_b_dt, P_tilde, tau_p_b, tau_z_b):
    """
    Linear derivative filter for afferent baroreceptor processing
    τ_p,b * dP_tilde/dt = P_b + τ_z,b * dP_b/dt - P_tilde

    From Albanese et al. 2016, based on Ursino & Magosso cardiovascular control model

    Args:
        P_b: Baroreceptor pressure (systemic arterial pressure) (mmHg)
        dP_b_dt: Rate of change of baroreceptor pressure (mmHg/s)
        P_tilde: Current output of linear filter (mmHg)
        tau_p_b: Time constant for real pole (s)
        tau_z_b: Time constant for real zero (s)

    Returns:
        dP_tilde_dt: Rate of change of filter output (mmHg/s)
    """
    dP_tilde_dt = (P_b + tau_z_b * dP_b_dt - P_tilde) / tau_p_b
    return dP_tilde_dt


def afferentActivity(P_tilde, P_n, f_ab_min, f_ab_max, k_ab):
    """
    Afferent baroreceptor activity (sigmoid function)
    f_ab = f_ab_min + f_ab_max * exp((P_tilde - P_n)/k_ab) / (1 + exp((P_tilde - P_n)/k_ab))

    From Albanese et al. 2016, cardiovascular control system

    Args:
        P_tilde: Output of linear derivative filter (mmHg)
        P_n: Pressure at central point of sigmoid (mmHg)
        f_ab_min: Lower saturation of frequency discharge (spikes/s)
        f_ab_max: Upper saturation of frequency discharge (spikes/s)
        k_ab: Parameter related to slope at central point (mmHg)

    Returns:
        f_ab: Afferent baroreceptor frequency (spikes/s)
    """
    exp_term = np.exp((P_tilde - P_n) / k_ab)
    f_ab = f_ab_min + f_ab_max * exp_term / (1 + exp_term)
    return f_ab