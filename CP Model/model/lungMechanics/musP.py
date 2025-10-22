import numpy as np


def musP(minP, b, Ti, Te, dt=None, Pmus_prev=None):
    """
    Muscle pressure pattern with derivative

    Based on Albanese et al. 2016, Equation 4:

    Pmus(t) = {
        (Pmus_min/Ti·Te) · t² + (Pmus_min·T/Ti·Te) · t    for t ∈ [0, Ti]
        Pmus_min · (1 - e^(-Te/τ)) · (e^(-(t-Ti)/τ) - e^(-Te/τ)) / (1 - e^(-Te/τ))  for t ∈ [Ti, T]
    }

    Returns:
    - Pmus: current muscle pressure
    - dP_mus: muscle pressure derivative (if dt and Pmus_prev provided)
    - tau: time constant
    """
    T = Ti + Te
    tau = Te / 5

    if b <= Ti:
        # Inspiratory phase - parabolic profile
        Pmus = ((-minP * b ** 2) + (minP * T * b)) / (Ti * Te)
    else:
        # Expiratory phase - exponential profile
        exp_term = np.exp(-(b - Ti) / tau) - np.exp(-Te / tau)
        denominator = 1 - np.exp(-Te / tau)
        Pmus = (minP * exp_term) / denominator

    # Calculate derivative if previous value provided
    if dt is not None and Pmus_prev is not None:
        dP_mus = (Pmus - Pmus_prev) / dt
    else:
        dP_mus = 0

    return Pmus, dP_mus, tau


def exerciseRespiratoryEffects(exercise_intensity, RR_0, Pmus_min_0, central_command_RR=0, central_command_Pmus=0):
    """
    Calculate exercise effects on respiratory parameters
    From Magosso & Ursino 2002 respiratory response model

    Exercise affects:
    1. Respiratory rate (RR)
    2. Respiratory muscle pressure amplitude (Pmus_min)

    Args:
        exercise_intensity: normalized exercise intensity (0-1)
        RR_0: baseline respiratory rate (breaths/min)
        Pmus_min_0: baseline respiratory muscle pressure amplitude (cmH2O)
        central_command_RR: central command contribution to RR
        central_command_Pmus: central command contribution to Pmus

    Returns:
        RR: exercise-modified respiratory rate
        Pmus_min: exercise-modified pressure amplitude
    """
    # Exercise increases both RR and pressure amplitude
    # Based on ventilatory response equations from Magosso & Ursino 2002

    # Respiratory rate increase with exercise
    exercise_RR_gain = 1.0 + exercise_intensity * 1.5  # Up to 150% increase
    RR = RR_0 * exercise_RR_gain + central_command_RR

    # Respiratory pressure amplitude increase with exercise
    exercise_Pmus_gain = 1.0 + exercise_intensity * 2.0  # Up to 200% increase
    Pmus_min = Pmus_min_0 * exercise_Pmus_gain + central_command_Pmus

    return RR, Pmus_min