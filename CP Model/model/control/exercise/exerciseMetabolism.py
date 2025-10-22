"""
exerciseMetabolism.py

Exercise-induced metabolic vasodilation.
Local vasodilation in active muscle beds during exercise.
Based on Magosso & Ursino (2002) Equations 25-26.
"""

import numpy as np


def exerciseMetabolicResponse(I, q_min, q_max, I_0_met, k_met, D_met, tau_met, x_met_prev, dt):
    """
    Exercise metabolic vasodilation with dynamics

    Static: φ_met(I) = q_min + q_max * exp((I - I_0)/k_met) / (1 + exp((I - I_0)/k_met))
    Dynamic: dx_met/dt = (1/τ_met) * (-x_met + φ_met(I - D_met))

    Parameters:
    -----------
    I : float
        Current exercise intensity (0-1)
    q_min : float
        Minimum metabolic response
    q_max : float
        Maximum metabolic response
    I_0_met : float
        Exercise intensity at central point
    k_met : float
        Slope parameter
    D_met : float
        Pure delay (s) - handle externally with delay buffer
    tau_met : float
        Time constant (s)
    x_met_prev : float
        Previous metabolic state
    dt : float
        Time step (s)

    Returns:
    --------
    tuple
        (x_met_new, phi_met_static)
    """
    # Static metabolic response
    if I <= 0:
        phi_met = q_min
    else:
        exp_term = np.exp((I - I_0_met) / k_met)
        phi_met = q_min + q_max * exp_term / (1 + exp_term)

    # Dynamic response
    dx_met_dt = (1 / tau_met) * (-x_met_prev + phi_met)
    x_met_new = x_met_prev + dx_met_dt * dt

    return x_met_new, phi_met


def oxygenConsumptionRate(I, M_O2_rest, g_M, tau_M, x_M_prev, dt):
    """
    Exercise-dependent oxygen consumption in active muscle

    M_O2 = M_O2_rest * (1 + x_M)
    dx_M/dt = (1/τ_M) * (-x_M + g_M * I)

    Parameters:
    -----------
    I : float
        Exercise intensity (0-1)
    M_O2_rest : float
        Resting O2 consumption rate (ml/s)
    g_M : float
        Exercise gain factor
    tau_M : float
        Time constant (s)
    x_M_prev : float
        Previous O2 consumption state
    dt : float
        Time step (s)

    Returns:
    --------
    tuple
        (M_O2_new, x_M_new)
    """
    # Dynamic O2 consumption
    dx_M_dt = (1 / tau_M) * (-x_M_prev + g_M * I)
    x_M_new = x_M_prev + dx_M_dt * dt

    # Final O2 consumption rate
    M_O2_new = M_O2_rest * (1 + x_M_new)

    return M_O2_new, x_M_new


def exerciseMetabolicVasodilation(exercise_intensity, q_min=1.87, q_max=20, I_0_met=0.4266, k_met=0.18, D_met=4,
                                  tau_met=10):
    """
    Exercise metabolic vasodilation in active muscle
    From Magosso & Ursino 2002, Equation 26
    """
    # Static sigmoidal response
    exp_term = np.exp((exercise_intensity - I_0_met) / k_met)
    q_met_static = (q_min + q_max * exp_term) / (1 + exp_term) - q_min

    return max(0, q_met_static)


def exerciseO2Consumption(exercise_intensity, M_O2_rest, g_M=40, tau_M=40):
    """
    Exercise O2 consumption in active muscle
    From Magosso & Ursino 2002, Equations 20-21

    M_am = M_am,n * (1 + x_M)
    dx_M/dt = (1/τ_M) * (-x_M + g_M * I)

    Args:
        exercise_intensity: Exercise level (0-1)
        M_O2_rest: Resting O2 consumption (ml/min)
        g_M: Metabolic gain factor (from Table 2)
        tau_M: Time constant (s, from Table 2)

    Returns:
        M_O2_exercise: O2 consumption during exercise (ml/min)
        x_M: Metabolic state variable
    """
    # Steady-state metabolic response
    x_M = g_M * exercise_intensity

    # Exercise O2 consumption
    M_O2_exercise = M_O2_rest * (1 + x_M)

    return M_O2_exercise, x_M


def exerciseO2ConsumptionDynamics(x_M, exercise_intensity, g_M=40, tau_M=40):
    """
    Dynamic response of exercise metabolism
    dx_M/dt = (1/τ_M) * (-x_M + g_M * I)
    """
    dx_M_dt = (1 / tau_M) * (-x_M + g_M * exercise_intensity)
    return dx_M_dt