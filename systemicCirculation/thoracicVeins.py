import numpy as np


def thoracicVeins(Qsv, Qev, Qmv, Qbv, Qhv, Vtv, Pra, Ppl, 
                  D1, K1, Vutv, D2, K2, Vtv_min, K_xp, K_xv,
                  KR, Vtv_max, Rtv_0):
    """
    Thoracic veins with nonlinear P-V relationship and variable resistance
    
    Albanese equations A15-A17, Equation 2, Equation 3:
    - A15: Volume derivative (5 inflows for Albanese)
    - A16: Outflow to right atrium
    - A17: Thoracic venous pressure
    - Eq 2: Nonlinear P-V relationship
    - Eq 3: Variable resistance
    
    Parameters:
    - Qsv, Qev, Qmv, Qbv, Qhv: flows from 5 venous beds
    - Vtv: thoracic veins volume
    - Pra: right atrial pressure
    - Ppl: pleural pressure
    - D1, K1, Vutv: nonlinear P-V parameters (upper branch)
    - D2, K2, Vtv_min: nonlinear P-V parameters (lower branch)
    - K_xp, K_xv: nonlinear P-V correction terms
    - KR, Vtv_max, Rtv_0: variable resistance parameters
    
    Returns:
    - dVtv: volume derivative (for RK45 integration)
    - Ptv: thoracic venous pressure
    - Qtv: outflow to right atrium
    - Rtv: variable resistance
    - Ptm_tv: transmural pressure
    """
    
    # Total inflow from 5 venous beds (A15 - Albanese has 5 beds)
    Qin_total = Qsv + Qev + Qmv + Qbv + Qhv
    
    # Calculate transmural pressure from nonlinear P-V (Equation 2)
    Ptm_tv = nonlinearPV(Vtv, D1, K1, Vutv, D2, K2, Vtv_min, K_xp, K_xv)
    
    # A17: Total pressure
    Ptv = Ppl + Ptm_tv
    
    # Calculate VARIABLE resistance (Equation 3)
    Rtv = variableResistance(Vtv, KR, Vtv_max, Rtv_0)
    
    # A16: Outflow to right atrium with variable resistance
    Qtv = (Ptv - Pra) / Rtv
    
    # A15: Volume derivative
    dVtv = Qin_total - Qtv
    
    return dVtv, Ptv, Qtv, Rtv, Ptm_tv


def nonlinearPV(Vtv, D1, K1, Vutv, D2, K2, Vtv_min, K_xp, K_xv):
    """
    Nonlinear pressure-volume relationship (Equation 2)
    
    Ptm,tv = { D1 + K1·(Vtv - Vu,tv) - ψ     if Vtv ≥ Vu,tv
             { D2 + K2·e^(Vtv/Vtv,min) - ψ   if Vtv < Vu,tv
    
    where ψ = K_xp/(e^(Vtv/K_xv) - 1)
    
    Parameters:
    - Vtv: thoracic veins volume
    - D1, K1, Vutv: upper branch parameters
    - D2, K2, Vtv_min: lower branch (collapsed) parameters
    - K_xp, K_xv: correction term parameters
    
    Returns:
    - Ptm_tv: transmural pressure
    """
    # Calculate ψ term
    psi = K_xp / (np.exp(Vtv / K_xv) - 1)
    
    if Vtv >= Vutv:
        # Upper branch (normal filling)
        Ptm_tv = D1 + K1 * (Vtv - Vutv) - psi
    else:
        # Lower branch (collapsed veins)
        Ptm_tv = D2 + K2 * np.exp(Vtv / Vtv_min) - psi
    
    return Ptm_tv


def variableResistance(Vtv, KR, Vtv_max, Rtv_0):
    """
    Variable resistance as function of volume (Equation 3)
    
    Rtv = KR * (Vtv_max / Vtv)^2 + Rtv_0
    
    where KR is a scaling factor, Vtv_max is the maximum volume,
    and Rtv_0 is an offset parameter.
    
    Parameters:
    - Vtv: thoracic veins volume
    - KR: scaling factor
    - Vtv_max: maximum volume
    - Rtv_0: offset resistance
    
    Returns:
    - Rtv: variable resistance
    """
    Rtv = KR * (Vtv_max / Vtv) ** 2 + Rtv_0
    return Rtv
