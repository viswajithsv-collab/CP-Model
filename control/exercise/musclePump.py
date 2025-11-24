"""
musclePump.py

Muscle pump effects during exercise.
Mechanical effects of rhythmic muscle contractions on venous return.
Based on Magosso & Ursino (2002) Equations 2-3 and 12.
"""

import numpy as np


def intramuscularPressure(t, I, A_max, T_contraction, duty_cycle=0.6):
    """
    Intramuscular pressure during exercise

    P_im = A * θ(t) where θ(t) is muscle activation

    Parameters:
    -----------
    t : float
        Current time (s)
    I : float
        Exercise intensity (0-1)
    A_max : float
        Maximum intramuscular pressure (mmHg)
    T_contraction : float
        Contraction cycle period (s)
    duty_cycle : float
        Fraction of cycle in contraction (default 0.6)

    Returns:
    --------
    float
        Intramuscular pressure (mmHg)
    """
    if I <= 0:
        return 0.0

    # Exercise-dependent amplitude
    A = A_max * I

    # Muscle activation pattern (half-sine during contraction)
    T_c = T_contraction * duty_cycle  # Contraction duration
    cycle_time = t % T_contraction

    if cycle_time <= T_c:
        # Contraction phase - half sine wave
        theta = np.sin(np.pi * cycle_time / T_c)
    else:
        # Relaxation phase
        theta = 0.0

    P_im = A * theta
    return P_im


def muscleVenousResistance(V_mv, I, k_mv, V_mv_max, R_mv_0):
    """
    Variable muscle venous resistance during exercise

    During exercise: R_mv = k_mv / V_mv
    At rest: R_mv = R_mv_0

    Parameters:
    -----------
    V_mv : float
        Current muscle venous volume (ml)
    I : float
        Exercise intensity (0-1)
    k_mv : float
        Resistance scaling factor (mmHg*s)
    V_mv_max : float
        Maximum muscle venous volume (ml)
    R_mv_0 : float
        Resting muscle venous resistance (mmHg*s/ml)

    Returns:
    --------
    float
        Muscle venous resistance (mmHg*s/ml)
    """
    if I <= 0:
        return R_mv_0
    else:
        # Variable resistance inversely proportional to volume
        R_mv = k_mv * (V_mv_max / V_mv) ** 2 + R_mv_0
        return R_mv


def venousVolumeEffect(P_im, V_mv_baseline, compliance_factor=0.1):
    """
    Effect of intramuscular pressure on venous volume

    Parameters:
    -----------
    P_im : float
        Intramuscular pressure (mmHg)
    V_mv_baseline : float
        Baseline muscle venous volume (ml)
    compliance_factor : float
        Venous compliance factor (ml/mmHg)

    Returns:
    --------
    float
        Change in venous volume due to muscle pump (ml)
    """
    # Compression reduces venous volume
    dV_pump = -compliance_factor * P_im * V_mv_baseline
    return dV_pump