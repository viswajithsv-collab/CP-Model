import numpy as np

def ventricleUnimodal(E_plus, E, Vold, Vu, Fin, Fout, kr, ke, P0, h, E_minus, LVV0, P_vb):
    """
    Ventricle model with unimodal ESP function

    Parameters:
    - E_plus: Steep positive elastance (replaces Emax)
    - E_minus: Reduced elastance (E-)
    - LVV0: Unstressed volume threshold
    - P_vb: Pressure bias/offset
    """
    # Volume integration (same as before)
    V = Vold + (Fin - Fout) * h

    # Calculate breakpoint volume
    breakpoint = (E_plus * LVV0 + P_vb) / (E_plus - E_minus)

    # Piecewise ESP calculation
    if V < LVV0:
        ESP = 0
    elif V <= breakpoint:
        ESP = E_plus * (V - LVV0)
    else:
        ESP = E_minus * V + P_vb

    # EDP (same as before)
    EDP = P0 * (np.exp(ke * V) - 1)

    # Final pressure calculation
    Pmax = E * ESP + (1 - E) * EDP
    R = kr * Pmax
    P = Pmax - R * Fout

    return V, P, Pmax, R