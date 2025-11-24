import numpy as np


def applyDelay(current_value, delay_buffer, dt, D):
    """
    Apply pure delay using circular buffer

    Args:
        current_value: Current signal value
        delay_buffer: List storing delayed values
        dt: Time step (s)
        D: Delay time (s)

    Returns:
        delayed_value: Signal from D seconds ago
    """
    delay_steps = int(D / dt)

    # Add current value to buffer
    delay_buffer.append(current_value)

    # Remove old values if buffer too long
    if len(delay_buffer) > delay_steps:
        delayed_value = delay_buffer.pop(0)
    else:
        delayed_value = delay_buffer[0]  # Use first available if buffer not full

    return delayed_value


def peripheralResistanceStatic(f_sp_delayed, f_es_min, G_R):
    """
    Static response of peripheral resistance to delayed sympathetic activity
    From Ursino 2000, Equations 30-32

    s_R = G_R * ln(f_sp(t - D_R) - f_es_min + 1) if f_sp >= f_es_min, else 0
    """
    if f_sp_delayed >= f_es_min:
        s_R = G_R * np.log(f_sp_delayed - f_es_min + 1)
    else:
        s_R = 0
    return s_R


def peripheralResistanceDynamics(dR, s_R, tau_R):
    """
    Dynamic response of peripheral resistance
    From Ursino 2000, Equations 30-32

    ddR/dt = (1/τ_R) * (-dR + s_R)
    """
    ddR_dt = (1 / tau_R) * (-dR + s_R)
    return ddR_dt


def venousVolumeStatic(f_sv_delayed, f_es_min, G_V):
    """
    Static response of venous unstressed volume to delayed sympathetic activity
    From Ursino 2000, Equations 30-32 (venous version)

    s_V = -G_V * ln(f_sv(t - D_V) - f_es_min + 1) if f_sv >= f_es_min, else 0
    """
    if f_sv_delayed >= f_es_min:
        s_V = -G_V * np.log(f_sv_delayed - f_es_min + 1)
    else:
        s_V = 0
    return s_V


def venousVolumeDynamics(dV, s_V, tau_V):
    """
    Dynamic response of venous unstressed volume
    From Ursino 2000, Equations 30-32 (venous version)

    ddV/dt = (1/τ_V) * (-dV + s_V)
    """
    ddV_dt = (1 / tau_V) * (-dV + s_V)
    return ddV_dt


def cardiacContractilityStatic(f_sh_delayed, f_es_min, G_E):
    """
    Static response of cardiac contractility to delayed sympathetic activity
    From Ursino 2000, Equations 33-35

    s_E = G_E * ln(f_sh(t - D_E) - f_es_min + 1) if f_sh >= f_es_min, else 0
    """
    if f_sh_delayed >= f_es_min:
        s_E = G_E * np.log(f_sh_delayed - f_es_min + 1)
    else:
        s_E = 0
    return s_E


def cardiacContractilityDynamics(dE, s_E, tau_E):
    """
    Dynamic response of cardiac contractility
    From Ursino 2000, Equations 33-35

    ddE/dt = (1/τ_E) * (-dE + s_E)
    """
    ddE_dt = (1 / tau_E) * (-dE + s_E)
    return ddE_dt