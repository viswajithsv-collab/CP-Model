"""
respiratoryPump.py

Respiratory pump effects during exercise.
Enhanced ventilation and its cardiovascular effects.
Based on Magosso & Ursino (2002) Equations 27-33.
"""

import numpy as np


def exerciseVentilationResponse(I, V_n, A, B, fast_fraction=0.45, tau_v=60,
                                dV_slow_prev=0, dt=0.01):
    """
    Exercise ventilatory response with fast and slow components

    V̇ = V̇_n + ΔV̇_fast + ΔV̇_slow
    ΔV̇_steady = A*I + B*I²
    ΔV̇_fast = 0.45 * ΔV̇_steady (immediate)
    dΔV̇_slow/dt = (1/τ_v) * (-ΔV̇_slow + 0.55 * ΔV̇_steady)
    """
    # Steady-state ventilation change
    dV_steady = A * I + B * I ** 2

    # Fast component (immediate)
    dV_fast = fast_fraction * dV_steady

    # Slow component (with dynamics)
    target_slow = (1 - fast_fraction) * dV_steady
    ddV_slow_dt = (1 / tau_v) * (-dV_slow_prev + target_slow)
    dV_slow_new = dV_slow_prev + ddV_slow_dt * dt

    # Total ventilation
    V_total = V_n + dV_fast + dV_slow_new

    return max(0, V_total), dV_fast, dV_slow_new


def intrathoracicPressure(VT, P_thor_min_n=-5, P_thor_max_n=-4, g_thor=6.8):
    """
    Exercise-dependent intrathoracic pressure variations
    """
    dVT = VT - 0.583  # Change from resting VT

    P_thor_min = P_thor_min_n - g_thor * dVT
    P_thor_max = P_thor_max_n + g_thor * dVT

    return P_thor_min, P_thor_max


def abdominalPressure(VT, P_abd_min_n=-2.5, P_abd_max_n=0, g_abd=3.39):
    """
    Exercise-dependent abdominal pressure variations
    """
    dVT = VT - 0.583  # Change from resting VT

    P_abd_min = P_abd_min_n - g_abd * dVT
    P_abd_max = P_abd_max_n + g_abd * dVT

    return P_abd_min, P_abd_max