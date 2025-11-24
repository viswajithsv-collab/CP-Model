import numpy as np


def cnsHypoxicResponse(Pa_O2, x_max, x_min, P_O2n, k_isc):
    """
    CNS hypoxic response static function
    From Magosso & Ursino (2001), Equations 4 & 6

    x(Pa_O2) = (x_min + x_max * exp((Pa_O2 - P_O2n)/k_isc)) / (1 + exp((Pa_O2 - P_O2n)/k_isc))

    Args:
        Pa_O2: Arterial oxygen pressure (mmHg)
        x_max: Upper saturation level (spikes/s)
        x_min: Lower saturation level (spikes/s)
        P_O2n: Central point of response (mmHg)
        k_isc: Slope parameter (mmHg)
    """
    exp_term = np.exp((Pa_O2 - P_O2n) / k_isc)
    x_response = (x_min + x_max * exp_term) / (1 + exp_term)
    return x_response


def cnsHypoxicDynamics(u_offset, Pa_O2, x_max, x_min, P_O2n, k_isc, tau_isc):
    """
    CNS hypoxic response dynamics
    From Magosso & Ursino (2001), Equation 5

    du/dt = (1/τ_isc) * (-u + x(Pa_O2))

    Args:
        u_offset: Current CNS offset term (spikes/s)
        Pa_O2: Arterial oxygen pressure (mmHg)
        x_max, x_min: Saturation levels (spikes/s)
        P_O2n: Central point (mmHg)
        k_isc: Slope parameter (mmHg)
        tau_isc: Time constant (s)
    """
    x_response = cnsHypoxicResponse(Pa_O2, x_max, x_min, P_O2n, k_isc)
    du_dt = (1 / tau_isc) * (-u_offset + x_response)
    return du_dt


def cnsCO2Response(Pa_CO2, Pa_CO2n, g_ccs):
    """
    CNS CO2 response static function
    From Magosso & Ursino (2001), Equation 6

    Linear response to CO2 changes

    Args:
        Pa_CO2: Current arterial CO2 pressure (mmHg)
        Pa_CO2n: Normal arterial CO2 pressure (mmHg)
        g_ccs: CO2 gain factor (spikes/s/mmHg)
    """
    response = g_ccs * (Pa_CO2 - Pa_CO2n)
    return response


def cnsCO2Dynamics(u_CO2, Pa_CO2, Pa_CO2n, g_ccs, tau_cc):
    """
    CNS CO2 response dynamics
    From Magosso & Ursino (2001), Equation 6

    du_CO2/dt = (1/τ_cc) * (-u_CO2 + g_ccs * (Pa_CO2 - Pa_CO2n))

    Args:
        u_CO2: Current CO2 offset term (spikes/s)
        Pa_CO2: Current arterial CO2 pressure (mmHg)
        Pa_CO2n: Normal arterial CO2 pressure (mmHg)
        g_ccs: CO2 gain factor (spikes/s/mmHg)
        tau_cc: Time constant (s)
    """
    response = cnsCO2Response(Pa_CO2, Pa_CO2n, g_ccs)
    du_CO2_dt = (1 / tau_cc) * (-u_CO2 + response)
    return du_CO2_dt


def cnsOffsetPeripheral(u_sp_n, u_hypoxic_sp, u_CO2_sp):
    """
    CNS offset term for sympathetic fibers to arterioles (peripheral)
    u_sp = u_sp_n - u_hypoxic_sp - u_CO2_sp
    """
    u_sp = u_sp_n - u_hypoxic_sp - u_CO2_sp
    return u_sp


def cnsOffsetVenous(u_sv_n, u_hypoxic_sv, u_CO2_sv):
    """
    CNS offset term for sympathetic fibers to veins
    u_sv = u_sv_n - u_hypoxic_sv - u_CO2_sv
    """
    u_sv = u_sv_n - u_hypoxic_sv - u_CO2_sv
    return u_sv


def cnsOffsetCardiac(u_sh_n, u_hypoxic_sh, u_CO2_sh):
    """
    CNS offset term for sympathetic fibers to heart
    u_sh = u_sh_n - u_hypoxic_sh - u_CO2_sh
    """
    u_sh = u_sh_n - u_hypoxic_sh - u_CO2_sh
    return u_sh