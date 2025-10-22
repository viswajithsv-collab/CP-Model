import numpy as np


def peripheralVentilation(dV_p, f_ac, f_ac_n, g_vp, tau_vp, D_vp):
    """
    Peripheral chemoreceptor contribution to ventilation
    From Magosso & Ursino (2001), Equation 17

    dΔV̇p/dt = (1/τvp) * (-ΔV̇p + gvp * [fac(t - Dvp) - fac,n])

    Args:
        dV_p: Current peripheral ventilation change (L/min)
        f_ac: Current peripheral chemoreceptor activity (spikes/s)
        f_ac_n: Basal chemoreceptor activity (spikes/s)
        g_vp: Peripheral gain factor (L/min/spikes/s)
        tau_vp: Peripheral time constant (s)
        D_vp: Peripheral delay (s) - handled externally
    """
    ddV_p_dt = (1 / tau_vp) * (-dV_p + g_vp * (f_ac - f_ac_n))
    return ddV_p_dt


def centralVentilation(dV_c, Pa_CO2, Pa_CO2_n, g_vc, tau_vc, D_vc):
    """
    Central chemoreceptor contribution to ventilation
    From Magosso & Ursino (2001), Equation 18

    dΔV̇c/dt = (1/τvc) * (-ΔV̇c + gvc * [PaCO2(t - Dvc) - PaCO2,n])

    Args:
        dV_c: Current central ventilation change (L/min)
        Pa_CO2: Current arterial CO2 pressure (mmHg)
        Pa_CO2_n: Normal arterial CO2 pressure (mmHg)
        g_vc: Central gain factor (L/min/mmHg)
        tau_vc: Central time constant (s)
        D_vc: Central delay (s) - handled externally
    """
    ddV_c_dt = (1 / tau_vc) * (-dV_c + g_vc * (Pa_CO2 - Pa_CO2_n))
    return ddV_c_dt


def totalVentilation(V_n, dV_p, dV_c):
    """
    Total ventilation from peripheral and central contributions
    From Magosso & Ursino (2001), Equation 16

    V̇ = V̇n + ΔV̇p + ΔV̇c

    Args:
        V_n: Basal ventilation (L/min)
        dV_p: Peripheral ventilation change (L/min)
        dV_c: Central ventilation change (L/min)
    """
    V_dot = V_n + dV_p + dV_c
    return max(0, V_dot)  # Ensure non-negative


def tidalVolume(V_dot):
    """
    Tidal volume from total ventilation
    From Magosso & Ursino (2001), Equation 19

    VT = 0.15 * (V̇ + 1)^0.65

    Args:
        V_dot: Total ventilation (L/min)
    """
    VT = 0.15 * ((V_dot + 1) ** 0.65)
    return VT


def respiratoryRate(V_dot, VT):
    """
    Respiratory rate from ventilation and tidal volume
    From Magosso & Ursino (2001), Equation 20

    RR = V̇/VT

    Args:
        V_dot: Total ventilation (L/min)
        VT: Tidal volume (L)
    """
    if VT > 0:
        RR = V_dot / VT
    else:
        RR = 0
    return RR


def lungStretchStatic(VT, G_ap):
    """
    Lung stretch receptor static response
    From Ursino & Magosso (2000), Equation 19

    w_ap(VT) = G_ap * VT

    Args:
        VT: Tidal volume (L)
        G_ap: Gain factor (spikes/s/L)
    """
    w_ap = G_ap * VT
    return w_ap


def lungStretchDynamics(f_ap, VT, G_ap, tau_p):
    """
    Lung stretch receptor dynamics
    From Ursino & Magosso (2000), Equation 20

    df_ap/dt = (1/τ_p) * (-f_ap + w_ap)

    Args:
        f_ap: Current lung stretch receptor activity (spikes/s)
        VT: Tidal volume (L)
        G_ap: Gain factor (spikes/s/L)
        tau_p: Time constant (s)
    """
    w_ap = lungStretchStatic(VT, G_ap)
    df_ap_dt = (1 / tau_p) * (-f_ap + w_ap)
    return df_ap_dt