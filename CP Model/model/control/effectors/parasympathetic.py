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


def heartPeriodSympatheticStatic(f_sh_delayed, f_es_min, G_T_s):
    """
    Sympathetic component of heart period control with delay
    From Ursino 2000, Equations 36-40

    s_T_s = G_T_s * ln(f_sh(t - D_T_s) - f_es_min + 1) if f_sh >= f_es_min, else 0
    """
    if f_sh_delayed >= f_es_min:
        s_T_s = G_T_s * np.log(f_sh_delayed - f_es_min + 1)
    else:
        s_T_s = 0
    return s_T_s


def heartPeriodSympatheticDynamics(dT_s, s_T_s, tau_T_s):
    """
    Sympathetic heart period dynamics
    From Ursino 2000, Equations 36-40

    ddT_s/dt = (1/τ_T_s) * (-dT_s + s_T_s)
    """
    ddT_s_dt = (1 / tau_T_s) * (-dT_s + s_T_s)
    return ddT_s_dt


def heartPeriodVagalStatic(f_v_delayed, G_T_v):
    """
    Vagal (parasympathetic) component of heart period control with delay
    From Ursino 2000, Equations 36-40

    s_T_v = G_T_v * f_v(t - D_T_v)
    """
    s_T_v = G_T_v * f_v_delayed
    return s_T_v


def heartPeriodVagalDynamics(dT_v, s_T_v, tau_T_v):
    """
    Vagal heart period dynamics
    From Ursino 2000, Equations 36-40

    ddT_v/dt = (1/τ_T_v) * (-dT_v + s_T_v)
    """
    ddT_v_dt = (1 / tau_T_v) * (-dT_v + s_T_v)
    return ddT_v_dt