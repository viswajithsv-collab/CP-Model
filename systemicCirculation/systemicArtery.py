import numpy as np


def systemicArteryRLC(Qin, Psa, Qsa, Pep, Rsa, Lsa, Csa, Vusa):
    """
    Systemic arteries with inertance (RLC model)
    
    Albanese equations A1-A3:
    - A1: Csa * dPsa/dt = Qin - Qsa
    - A2: Lsa * dQsa/dt = Psa - Pep - Rsa*Qsa
    - A3: Vsa = Csa*Psa + Vusa
    
    Parameters:
    - Qin: inflow from left ventricle (aortic valve)
    - Psa: systemic arterial pressure
    - Qsa: systemic arterial flow
    - Pep: equivalent peripheral pressure (from peripheral distribution)
    - Rsa: systemic arterial resistance
    - Lsa: systemic arterial inertance
    - Csa: systemic arterial compliance
    - Vusa: unstressed volume
    
    Returns:
    - dPsa: pressure derivative (for RK45 integration)
    - dQsa: flow derivative (for RK45 integration)
    - Vsa: systemic arterial volume (instantaneous)
    """
    # A2: Flow derivative
    dQsa = (Psa - Pep - Rsa * Qsa) / Lsa
    
    # A1: Pressure derivative
    dPsa = (Qin - Qsa) / Csa
    
    # A3: Volume (instantaneous calculation)
    Vsa = Csa * Psa + Vusa
    
    return dPsa, dQsa, Vsa


def systemicArteryRC(Qin, Psa, Pep, Rsa, Csa, Vusa=0):
    """
    Systemic arteries (simplified RC model without inertance)
    
    Albanese equation A1 (simplified):
    - Csa * dPsa/dt = Qin - (Psa - Pep)/Rsa
    
    Parameters:
    - Qin: inflow from left ventricle
    - Psa: systemic arterial pressure
    - Pep: equivalent peripheral pressure
    - Rsa: systemic arterial resistance
    - Csa: systemic arterial compliance
    - Vusa: unstressed volume
    
    Returns:
    - dPsa: pressure derivative (for RK45 integration)
    - Qsa: algebraic flow (instantaneous)
    - Vsa: systemic arterial volume (instantaneous)
    """
    # Algebraic flow (no inertance)
    Qsa = (Psa - Pep) / Rsa
    
    # A1: Pressure derivative
    dPsa = (Qin - Qsa) / Csa
    
    # A3: Volume (instantaneous calculation)
    Vsa = Csa * Psa + Vusa
    
    return dPsa, Qsa, Vsa
