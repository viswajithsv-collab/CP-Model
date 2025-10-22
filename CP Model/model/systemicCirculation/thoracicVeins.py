import numpy as np


def thoracicVeinsResistance(Vtv, KR, Vtv_max, Rtv_0):
    """
    Thoracic veins variable resistance (Equation 3)

    Parameters:
    - Vtv: current thoracic veins volume
    - KR: scaling factor
    - Vtv_max: maximum volume
    - Rtv_0: offset resistance

    Returns:
    - Rtv: variable resistance
    """
    Rtv = KR * (Vtv_max / Vtv) ** 2 + Rtv_0
    return Rtv


def thoracicVeins(Qsv, Qev, Qamv, Qrmv, Qbv, Qhv, Vtv_old, Pra, Ppl, h, D1, K1, Vu_tv, D2, K2, Vtv_min, K_xp, K_xv, KR,
                  Vtv_max, Rtv_0):
    """
        Thoracic veins with nonlinear P-V relationship - NOW 6 INFLOWS

        Based on equations A15-A17 and Equation 2:
        - A15: dVtv/dt = Σj Qjv - Qtv (NOW 6 TERMS)
        - A16: Qtv = (Ptv - Pra)/Rtv
        - A17: Ptv = Ppl + Ptm,tv
        - Eq 2: Nonlinear P-V relationship

        Parameters:
        - Qsv, Qev, Qamv, Qrmv, Qbv, Qhv: flows from 6 venous beds (A13)
        - Vtv_old: previous thoracic veins volume
        - Pra: right atrial pressure
        - Ppl: pleural pressure
        - h: time step
        - D1, K1, D2, K2, etc.: nonlinear P-V parameters (Equation 2)

        Returns:
        - Vtv_new: updated thoracic veins volume
        - Ptv: thoracic veins pressure
        - Qtv: outflow to right atrium
        - Ptm_tv: transmural pressure
    """

    # Total inflow from 6 venous beds (UPDATED)
    Qin_total = Qsv + Qev + Qamv + Qrmv + Qbv + Qhv

    # Calculate transmural pressure from nonlinear P-V (Equation 2)
    Ptm_tv = nonlinearPV(Vtv_old, D1, K1, Vu_tv, D2, K2, Vtv_min, K_xp, K_xv)
    Ptv = Ppl + Ptm_tv  # A17

    # Calculate VARIABLE resistance (Equation 3)
    Rtv = thoracicVeinsResistance(Vtv_old, KR, Vtv_max, Rtv_0)

    # Outflow with variable resistance (A16)
    Qtv = (Ptv - Pra) / Rtv

    # Volume integration (A15)
    dVtv = Qin_total - Qtv
    Vtv_new = Vtv_old + dVtv * h

    return Vtv_new, Ptv, Qtv, Rtv, Ptm_tv


def nonlinearPV(Vtv, D1, K1, Vu_tv, D2, K2, Vtv_min, K_xp, K_xv):
    """
    Nonlinear pressure-volume relationship (Equation 2)

    Ptm,tv = { D1 + K1·(Vtv - Vu,tv) - ψ     if Vtv ≥ Vu,tv
             { D2 + K2·e^(Vtv/Vtv,min) - ψ   if Vtv < Vu,tv

    where ψ = K_xp/(e^(Vtv/K_xv) - 1)
    """

    # Calculate ψ term
    psi = K_xp / (np.exp(Vtv / K_xv) - 1)

    if Vtv >= Vu_tv:
        # Upper branch
        Ptm_tv = D1 + K1 * (Vtv - Vu_tv) - psi
    else:
        # Lower branch (collapsed)
        Ptm_tv = D2 + K2 * np.exp(Vtv / Vtv_min) - psi

    return Ptm_tv