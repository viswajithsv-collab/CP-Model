def pulmonaryArtery(Qin, Ppa, Ppp, Rpa, Cpa, Vu_pa, P_thor=0, dP_thor=0):
    """
    Pulmonary artery with optional intrathoracic pressure reference (A18-A20)

    Based on:
    - A18: Cpa * d(Ppa - P_thor)/dt = Qrv,o - Qpa
    - A19: Qpa = (Ppa - Ppp)/Rpa (flow out)
    - A20: Vpa = Cpa * (Ppa - P_thor) + Vu,pa (volume)

    Optional parameters (default to 0 for non-exercise simulations):
    - P_thor: intrathoracic pressure (mmHg) [default: 0]
    - dP_thor: intrathoracic pressure derivative (mmHg/s) [default: 0]
    """
    # A19: Outflow to pulmonary peripheral (unchanged)
    Qpa = (Ppa - Ppp) / Rpa

    # A18: Pressure derivative with optional intrathoracic reference
    # When P_thor=0 and dP_thor=0, reduces to original equation
    dPpa = (Qin - Qpa) / Cpa + dP_thor

    # A20: Volume with optional intrathoracic reference
    # When P_thor=0, reduces to original equation
    Vpa = Cpa * (Ppa - P_thor) + Vu_pa

    return dPpa, Qpa, Vpa