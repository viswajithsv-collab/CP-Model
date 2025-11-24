import numpy as np


def sympatheticPeripheral(f_ab, f_ac, f_ap, u_sp, W_b_sp, W_c_sp, W_p_sp, k_es, f_es_inf, f_es_0, f_es_max, gamma_sp=0):
    """
    Sympathetic activity to peripheral arterioles with central command
    From Magosso & Ursino 2001, Equation 21 + Magosso & Ursino 2002, Equation 15

    f_sp = [base_response] + γsp(I)
    """
    # Weighted sum of afferent inputs with CNS offset
    weighted_input = -W_b_sp * f_ab + W_c_sp * f_ac - W_p_sp * f_ap - u_sp

    # Exponential response
    exp_term = np.exp(k_es * weighted_input)
    f_sp_base = f_es_inf + (f_es_0 - f_es_inf) * exp_term

    # Add central command term (Magosso & Ursino 2002, Fig 2)
    f_sp = f_sp_base + gamma_sp

    # Apply saturation
    f_sp = min(f_sp, f_es_max)
    return f_sp


def sympatheticVenous(f_ab, f_ac, f_ap, u_sv, W_b_sv, W_c_sv, W_p_sv, k_es, f_es_inf, f_es_0, f_es_max, gamma_sv=0):
    """
    Sympathetic activity to veins with central command
    """
    weighted_input = -W_b_sv * f_ab + W_c_sv * f_ac - W_p_sv * f_ap - u_sv
    exp_term = np.exp(k_es * weighted_input)
    f_sv_base = f_es_inf + (f_es_0 - f_es_inf) * exp_term

    f_sv = f_sv_base + gamma_sv
    f_sv = min(f_sv, f_es_max)
    return f_sv


def sympatheticCardiac(f_ab, f_ac, u_sh, W_b_sh, W_c_sh, k_es, f_es_inf, f_es_0, f_es_max, gamma_sh=0):
    """
    Sympathetic activity to heart with central command
    """
    weighted_input = -W_b_sh * f_ab + W_c_sh * f_ac - u_sh
    exp_term = np.exp(k_es * weighted_input)
    f_sh_base = f_es_inf + (f_es_0 - f_es_inf) * exp_term

    f_sh = f_sh_base + gamma_sh
    f_sh = min(f_sh, f_es_max)
    return f_sh


def parasympatheticVagal(f_ab, f_ac, f_ap, f_ab_0, u_v, W_c_v, W_p_v, k_ev, f_ev_inf, f_ev_0, gamma_v=0):
    """
    Parasympathetic (vagal) activity to heart with central command
    Note: Central command inhibits vagal activity
    """
    exp_term = np.exp((f_ab - f_ab_0) / k_ev)
    baroreceptor_term = (f_ev_0 + f_ev_inf * exp_term) / (1 + exp_term)

    f_v_base = baroreceptor_term + W_c_v * f_ac - W_p_v * f_ap - u_v

    # Central command inhibits vagus (subtract)
    f_v = f_v_base - gamma_v
    f_v = max(0, f_v)
    return f_v