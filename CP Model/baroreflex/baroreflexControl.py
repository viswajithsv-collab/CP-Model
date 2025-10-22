import numpy as np

def afferentPathway(Paff, Pn, fmin, fmax, ka):
    """
    Afferent baroreceptor pathway
    Sigmoid function relating pressure to firing rate
    """
    e = np.exp((Paff - Pn) / ka)
    Nr = fmin + fmax * e
    Dr = 1 + e
    fcs = Nr / Dr
    return fcs

def efferentSympathetic(f, f0, finf, k):
    """
    Efferent sympathetic pathway
    Exponential decay function
    """
    fes = finf + (f0 - finf) * np.exp(-k * f)
    return fes

def efferentVagal(f, fc0, f0, finf, k):
    """
    Efferent vagal pathway
    Sigmoid function for parasympathetic control
    """
    e = np.exp((f - fc0) / k)
    Nr = f0 + finf * e
    Dr = 1 + e
    fev = Nr / Dr
    return fev

def effectorSympathetic(G, f, t, D, fmin):
    """
    Sympathetic effector with time delay
    Logarithmic gain with threshold
    """
    if f < fmin:
        sigma = 0
    elif t < D:
        sigma = G * np.log(-fmin + 1)
    else:
        sigma = G * np.log(f - fmin + 1)
    return sigma

def effectorVagal(G, f, t, D):
    """
    Vagal effector with time delay
    Linear gain with delay
    """
    if t < D:
        vsigma = 0
    else:
        vsigma = G * f
    return vsigma

def linearDerivative(Pcs, dPcs, Paff, taup, tauz):
    """
    Linear derivative filter for afferent processing
    First-order system with derivative term
    """
    dPaff = (Pcs + tauz * dPcs - Paff) / taup
    return dPaff

def regulation(deltheta, sigma, tau):
    """
    First-order regulation dynamics
    Controls how effector signals regulate physiological variables
    """
    ddeltheta = (-deltheta + sigma) / tau
    return ddeltheta