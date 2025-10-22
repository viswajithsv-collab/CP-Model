import numpy as np


def systemicArteriesRLC(Qin, Psa_old, Qsa_old, Pep, Rsa, Lsa, Csa, Vusa, h):
    """Systemic arteries WITH inertance (L)"""
    # A2: dQsa/dt = (Psa - Pep - Rsa * Qsa) / Lsa
    dQsa = (Psa_old - Pep - Rsa * Qsa_old) / Lsa
    Qsa_new = Qsa_old + dQsa * h

    # A1: dPsa/dt = (Qin - Qsa) / Csa
    dPsa = (Qin - Qsa_old) / Csa
    Psa_new = Psa_old + dPsa * h

    # A3: Volume
    Vsa = Csa * Psa_new + Vusa

    return Psa_new, Qsa_new, Vsa


def systemicArteriesRC(Qin, Psa, Psp, Rsa, Csa, Vusa=0):
    """Systemic artery pressure derivative (RC model)"""
    dPsa = (Qin - (Psa - Psp) / Rsa) / Csa
    Vsa = Csa * Psa + Vusa
    return dPsa, Vsa