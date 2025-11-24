"""
centralCommand.py

Central command effects on cardiovascular control.
Direct neural drive from motor cortex during exercise.
Based on Magosso & Ursino (2002) Equation 15.
"""

import numpy as np


def centralCommandSympathetic(I, gamma_max, I_0, k_cc):
    """
    Central command effect on sympathetic activity

    Sigmoidal function: γ = γ_max * exp((I - I_0)/k_cc) / (1 + exp((I - I_0)/k_cc))

    Parameters:
    -----------
    I : float
        Exercise intensity (0-1)
    gamma_max : float
        Maximum central command effect (spikes/s)
    I_0 : float
        Exercise intensity at central point of sigmoid
    k_cc : float
        Slope parameter

    Returns:
    --------
    float
        Central command sympathetic effect (spikes/s)
    """
    if I <= 0:
        return 0.0

    exp_term = np.exp((I - I_0) / k_cc)
    gamma = gamma_max * exp_term / (1 + exp_term)
    return gamma


def centralCommandVagal(I, gamma_v_max, I_0_v, k_cc_v):
    """
    Central command effect on vagal activity (inhibitory)

    Parameters:
    -----------
    I : float
        Exercise intensity (0-1)
    gamma_v_max : float
        Maximum vagal inhibition (spikes/s)
    I_0_v : float
        Exercise intensity at central point
    k_cc_v : float
        Slope parameter

    Returns:
    --------
    float
        Central command vagal inhibition (spikes/s)
    """
    if I <= 0:
        return 0.0

    exp_term = np.exp((I - I_0_v) / k_cc_v)
    gamma_v = gamma_v_max * exp_term / (1 + exp_term)
    return gamma_v