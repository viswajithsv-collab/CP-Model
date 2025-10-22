import numpy as np


def brain_conductance(G_bpn, x_b_O2, x_b_CO2):
    """
    Brain peripheral conductance with O2 and CO2 autoregulation
    G_bp = G_bpn * (1 + x_b,O2 + x_b,CO2)

    Args:
        G_bpn: Basal brain peripheral conductance
        x_b_O2: Brain O2 autoregulation state variable
        x_b_CO2: Brain CO2 autoregulation state variable
    """
    G_bp = G_bpn * (1 + x_b_O2 + x_b_CO2)
    return G_bp


def brain_O2_dynamics(x_b_O2, C_vb_O2, C_vb_O2n, g_b_O2, tau_O2):
    """
    Brain O2 autoregulation dynamics
    dx_b,O2/dt = (1/τ_O2) * [-x_b,O2 - g_b,O2 * (C_vb,O2 - C_vb,O2n)]

    Args:
        x_b_O2: Current brain O2 state variable
        C_vb_O2: Current venous O2 concentration leaving brain
        C_vb_O2n: Normal venous O2 concentration leaving brain
        g_b_O2: Brain O2 gain factor
        tau_O2: O2 response time constant
    """
    dx_b_O2_dt = (1 / tau_O2) * (-x_b_O2 - g_b_O2 * (C_vb_O2 - C_vb_O2n))
    return dx_b_O2_dt


def brain_CO2_response(Pa_CO2, Pa_CO2n, A, B, C, D):
    """
    Brain CO2 static response function
    F_b(Pa_CO2) = [A + B/(1 + C*exp(D*log(Pa_CO2)))] / [A + B/(1 + C*exp(D*log(Pa_CO2n)))] - 1

    Args:
        Pa_CO2: Current arterial CO2 pressure
        Pa_CO2n: Normal arterial CO2 pressure
        A, B, C, D: Brain CO2 response parameters
    """
    numerator = A + B / (1 + C * np.exp(D * np.log(Pa_CO2)))
    denominator = A + B / (1 + C * np.exp(D * np.log(Pa_CO2n)))
    F_b = (numerator / denominator) - 1
    return F_b


def brain_CO2_dynamics(x_b_CO2, Pa_CO2, Pa_CO2n, A, B, C, D, tau_CO2):
    """
    Brain CO2 autoregulation dynamics
    dx_b,CO2/dt = (1/τ_CO2) * [-x_b,CO2 + F_b(Pa_CO2)]

    Args:
        x_b_CO2: Current brain CO2 state variable
        Pa_CO2: Current arterial CO2 pressure
        Pa_CO2n: Normal arterial CO2 pressure
        A, B, C, D: Brain CO2 response parameters
        tau_CO2: CO2 response time constant
    """
    F_b = brain_CO2_response(Pa_CO2, Pa_CO2n, A, B, C, D)
    dx_b_CO2_dt = (1 / tau_CO2) * (-x_b_CO2 + F_b)
    return dx_b_CO2_dt


def coronary_O2_dynamics(x_h_O2, C_vh_O2, C_vh_O2n, g_h_O2, tau_O2):
    """
    Coronary O2 autoregulation dynamics
    dx_h,O2/dt = (1/τ_O2) * [-x_h,O2 - g_h,O2 * (C_vh,O2 - C_vh,O2n)]

    Args:
        x_h_O2: Current coronary O2 state variable
        C_vh_O2: Current venous O2 concentration leaving heart
        C_vh_O2n: Normal venous O2 concentration leaving heart
        g_h_O2: Coronary O2 gain factor
        tau_O2: O2 response time constant
    """
    dx_h_O2_dt = (1 / tau_O2) * (-x_h_O2 - g_h_O2 * (C_vh_O2 - C_vh_O2n))
    return dx_h_O2_dt


def coronary_CO2_response(Pa_CO2, Pa_CO2n, k_h_CO2):
    """
    Coronary CO2 static response function
    F_h(Pa_CO2) = [1 - exp((Pa_CO2 - Pa_CO2n)/k_h,CO2)] / [1 + exp((Pa_CO2 - Pa_CO2n)/k_h,CO2)]

    Args:
        Pa_CO2: Current arterial CO2 pressure
        Pa_CO2n: Normal arterial CO2 pressure
        k_h_CO2: Coronary CO2 sensitivity parameter
    """
    exp_term = np.exp((Pa_CO2 - Pa_CO2n) / k_h_CO2)
    F_h = (1 - exp_term) / (1 + exp_term)
    return F_h


def coronary_CO2_dynamics(x_h_CO2, Pa_CO2, Pa_CO2n, k_h_CO2, tau_CO2):
    """
    Coronary CO2 autoregulation dynamics
    dx_h,CO2/dt = (1/τ_CO2) * [-x_h,CO2 + F_h(Pa_CO2)]

    Args:
        x_h_CO2: Current coronary CO2 state variable
        Pa_CO2: Current arterial CO2 pressure
        Pa_CO2n: Normal arterial CO2 pressure
        k_h_CO2: Coronary CO2 sensitivity parameter
        tau_CO2: CO2 response time constant
    """
    F_h = coronary_CO2_response(Pa_CO2, Pa_CO2n, k_h_CO2)
    dx_h_CO2_dt = (1 / tau_CO2) * (-x_h_CO2 + F_h)
    return dx_h_CO2_dt


def muscle_O2_dynamics(x_m_O2, C_vm_O2, C_vm_O2n, g_m_O2, tau_O2):
    """
    Muscle O2 autoregulation dynamics
    dx_m,O2/dt = (1/τ_O2) * [-x_m,O2 - g_m,O2 * (C_vm,O2 - C_vm,O2n)]

    Args:
        x_m_O2: Current muscle O2 state variable
        C_vm_O2: Current venous O2 concentration leaving muscle
        C_vm_O2n: Normal venous O2 concentration leaving muscle
        g_m_O2: Muscle O2 gain factor
        tau_O2: O2 response time constant
    """
    dx_m_O2_dt = (1 / tau_O2) * (-x_m_O2 - g_m_O2 * (C_vm_O2 - C_vm_O2n))
    return dx_m_O2_dt


def muscle_CO2_response(Pa_CO2, Pa_CO2n, k_m_CO2):
    """
    Muscle CO2 static response function
    F_m(Pa_CO2) = [1 - exp((Pa_CO2 - Pa_CO2n)/k_m,CO2)] / [1 + exp((Pa_CO2 - Pa_CO2n)/k_m,CO2)]

    Args:
        Pa_CO2: Current arterial CO2 pressure
        Pa_CO2n: Normal arterial CO2 pressure
        k_m_CO2: Muscle CO2 sensitivity parameter
    """
    exp_term = np.exp((Pa_CO2 - Pa_CO2n) / k_m_CO2)
    F_m = (1 - exp_term) / (1 + exp_term)
    return F_m


def muscle_CO2_dynamics(x_m_CO2, Pa_CO2, Pa_CO2n, k_m_CO2, tau_CO2):
    """
    Muscle CO2 autoregulation dynamics
    dx_m,CO2/dt = (1/τ_CO2) * [-x_m,CO2 + F_m(Pa_CO2)]

    Args:
        x_m_CO2: Current muscle CO2 state variable
        Pa_CO2: Current arterial CO2 pressure
        Pa_CO2n: Normal arterial CO2 pressure
        k_m_CO2: Muscle CO2 sensitivity parameter
        tau_CO2: CO2 response time constant
    """
    F_m = muscle_CO2_response(Pa_CO2, Pa_CO2n, k_m_CO2)
    dx_m_CO2_dt = (1 / tau_CO2) * (-x_m_CO2 + F_m)
    return dx_m_CO2_dt