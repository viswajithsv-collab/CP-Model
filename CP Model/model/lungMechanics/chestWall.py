def chestWall(Pl, Pt, Rlt, Ccw, dP_mus):
    """
    Chest wall / pleural pressure derivative (A34)
    From Albanese et al. 2016, Equation A34:

    Ccw · d(Ppl - Pmus)/dt = (Pl - Ptr)/Rlt
    """
    Qin = (Pl - Pt) / Rlt
    dP_pl = dP_mus + Qin / Ccw
    return dP_pl


def intrathoracicPressure(s, Ti, Te, Tresp, Pthor_min, Pthor_max):
    """
    Intrathoracic pressure pattern during exercise
    From Magosso & Ursino 2002, equations (4) and (5):

    During inspiration (0 ≤ s ≤ Ti/Tresp):
    Pthor(t) = Pthor_max - (Pthor_max - Pthor_min) × (s × Tresp / Ti)

    During expiration (Ti/Tresp < s ≤ (Ti + Te)/Tresp):
    Pthor(t) = Pthor_min + (Pthor_max - Pthor_min) × ((s × Tresp - Ti) / Te)

    During pause ((Ti + Te)/Tresp < s ≤ 1):
    Pthor(t) = Pthor_max

    Args:
        s: dimensionless respiratory cycle fraction (0-1)
        Ti: inspiration time (s)
        Te: expiration time (s)
        Tresp: total respiratory period (s)
        Pthor_min: minimum intrathoracic pressure (mmHg)
        Pthor_max: maximum intrathoracic pressure (mmHg)
    """
    Ti_frac = Ti / Tresp
    Te_frac = Te / Tresp

    if s <= Ti_frac:
        # Inspiration - linear decrease
        Pthor = Pthor_max - (Pthor_max - Pthor_min) * (s / Ti_frac)
    elif s <= (Ti_frac + Te_frac):
        # Expiration - linear increase
        s_exp = (s - Ti_frac) / Te_frac
        Pthor = Pthor_min + (Pthor_max - Pthor_min) * s_exp
    else:
        # Respiratory pause
        Pthor = Pthor_max

    return Pthor


def abdominalPressure(s, Ti, Te, Tresp, Pabd_min, Pabd_max):
    """
    Abdominal pressure pattern during exercise
    From Magosso & Ursino 2002, equations (4) and (5):

    During first half inspiration (0 ≤ s ≤ Ti/(2×Tresp)):
    Pabd(t) = Pabd_max - (Pabd_max - Pabd_min) × (2s × Tresp / Ti)

    During second half inspiration (Ti/(2×Tresp) < s ≤ Ti/Tresp):
    Pabd(t) = Pabd_min

    During expiration (Ti/Tresp < s ≤ (Ti + Te)/Tresp):
    Pabd(t) = Pabd_min + (Pabd_max - Pabd_min) × ((s × Tresp - Ti) / Te)

    During pause ((Ti + Te)/Tresp < s ≤ 1):
    Pabd(t) = Pabd_max
    """
    Ti_frac = Ti / Tresp
    Te_frac = Te / Tresp
    Ti_half_frac = Ti_frac / 2

    if s <= Ti_half_frac:
        # First half inspiration - linear decrease
        Pabd = Pabd_max - (Pabd_max - Pabd_min) * (s / Ti_half_frac)
    elif s <= Ti_frac:
        # Second half inspiration - constant minimum
        Pabd = Pabd_min
    elif s <= (Ti_frac + Te_frac):
        # Expiration - linear increase
        s_exp = (s - Ti_frac) / Te_frac
        Pabd = Pabd_min + (Pabd_max - Pabd_min) * s_exp
    else:
        # Respiratory pause
        Pabd = Pabd_max

    return Pabd