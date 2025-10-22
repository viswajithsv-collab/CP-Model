"""
exerciseIntensity.py

Main exercise intensity controller and coordination.
Based on Magosso & Ursino (2002) exercise model.
"""


def exerciseInput(I):
    """
    Normalize and validate exercise intensity

    Parameters:
    -----------
    I : float
        Exercise intensity (0 = rest, 1 = max aerobic threshold)

    Returns:
    --------
    float
        Validated exercise intensity
    """
    return max(0.0, min(1.0, I))


def exerciseOnset(t, t_start, t_ramp=0):
    """
    Exercise onset pattern (step or ramp)

    Parameters:
    -----------
    t : float
        Current time (s)
    t_start : float
        Exercise start time (s)
    t_ramp : float
        Ramp duration (s), 0 = step input

    Returns:
    --------
    float
        Exercise activation factor (0-1)
    """
    if t < t_start:
        return 0.0
    elif t_ramp == 0:
        return 1.0  # Step onset
    else:
        # Linear ramp
        ramp_progress = (t - t_start) / t_ramp
        return min(1.0, ramp_progress)