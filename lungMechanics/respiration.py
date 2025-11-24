def respiration(t, RR, IE, exercise_intensity=0):
    """
    Respiratory timing with exercise effects (Equation 5 + Magosso & Ursino 2002)

    From Magosso & Ursino 2002, equations (7) and (8):
    Ti/Tresp = 0.4 + 0.1·I  (for I ≤ 0.2)
    Ti/Tresp = 0.6 - 0.1·I  (for 0.2 < I ≤ 1)

    Te/Tresp = 0.35 + 1.15·I  (for I ≤ 0.2)
    Te/Tresp = 0.6 - 0.1·I   (for 0.2 < I ≤ 1)
    """
    # Exercise-modified timing fractions (Magosso & Ursino 2002, Eq 7-8)
    if exercise_intensity <= 0.2:
        Ti_fraction = 0.4 + 0.1 * exercise_intensity
        Te_fraction = 0.35 + 1.15 * exercise_intensity
    else:
        Ti_fraction = 0.6 - 0.1 * exercise_intensity
        Te_fraction = 0.6 - 0.1 * exercise_intensity

    # Base respiratory period
    T = 60.0 / RR

    # Exercise-modified timing
    Ti = T * Ti_fraction
    Te = T * Te_fraction

    # Current phase
    b = t % T

    return b, Ti, Te


def respiratoryPressureAmplitudes(exercise_intensity, base_Pthor_min_n, base_Pthor_max_n,
                                  base_Pabd_min_n, base_Pabd_max_n, gthor, gabd, delta_VT):
    """
    Exercise-dependent respiratory pressure amplitudes
    From Magosso & Ursino 2002, equations (9) and (10):

    Pthor_min = Pthor_min_n - gthor·ΔVT(I)
    Pthor_max = Pthor_max_n + gthor·ΔVT(I)
    Pabd_min = Pabd_min_n - gabd·ΔVT(I)
    Pabd_max = Pabd_max_n + gabd·ΔVT(I)
    """
    # Exercise-modified pressure extremes (Eq 9-10)
    Pthor_min = base_Pthor_min_n - gthor * delta_VT
    Pthor_max = base_Pthor_max_n + gthor * delta_VT
    Pabd_min = base_Pabd_min_n - gabd * delta_VT
    Pabd_max = base_Pabd_max_n + gabd * delta_VT

    return Pthor_min, Pthor_max, Pabd_min, Pabd_max