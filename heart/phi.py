import numpy as np

def phi(t, HR, alpha, n):
    """
    Heart activation function (normalized)

    Parameters:
    - t: time
    - HR: heart rate
    - alpha: [alpha1, alpha2] timing parameters
    - n: [n1, n2] shape parameters

    Returns:
    - En: normalized activation (0-1)
    """
    Tc = 60.0 / HR
    tm = t % Tc
    x = tm / Tc
    a1 = x / alpha[0]
    a2 = x / alpha[1]

    m = a1 ** n[0]
    o = a2 ** n[1]

    p = m / (1 + m)
    q = 1 / (1 + o)

    z = p * q
    mEn = np.max(z)

    En = z / mEn
    return En