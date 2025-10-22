import numpy as np

def ventricleConventional(Emax, E, Vold, Vu, Fin, Fout, kr, ke, P0, h):
    """Conventional linear ESP ventricle model"""
    V = Vold + (Fin - Fout) * h
    ESP = Emax * (V - Vu)  # Linear ESP
    EDP = P0 * (np.exp(ke * V) - 1)
    Pmax = E * ESP + (1 - E) * EDP
    R = kr * Pmax
    P = Pmax - R * Fout
    return V, P, Pmax, R