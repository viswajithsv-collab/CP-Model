def pulmonaryVascular(Ppa, Ppvb, Ppv, Rpa, Rpp, Rps, Cpp, Cps, Vu_pp, Vu_ps, P_thor=0, dP_thor=0):
    """
    Pulmonary vascular with optional intrathoracic pressure reference (A21-A26)

    Optional parameters (default to 0 for non-exercise simulations):
    - P_thor: intrathoracic pressure (mmHg) [default: 0]
    - dP_thor: intrathoracic pressure derivative (mmHg/s) [default: 0]
    """
    # Inflow from pulmonary arteries
    Fin = (Ppa - Ppvb) / Rpa

    # A22: Peripheral flow (gas exchange)
    Qpp = (Ppvb - Ppv) / Rpp

    # A23: Shunt flow (bypasses gas exchange)
    Qps = (Ppvb - Ppv) / Rps

    # A21: Pressure derivative with optional intrathoracic reference
    # When dP_thor=0, reduces to original equation
    Ctotal = Cpp + Cps
    dPpvb = (Fin - Qpp - Qps) / Ctotal + dP_thor

    # A25, A26: Volumes with optional intrathoracic reference
    # When P_thor=0, reduces to original equations
    Vpp = Cpp * (Ppvb - P_thor) + Vu_pp
    Vps = Cps * (Ppvb - P_thor) + Vu_ps

    return dPpvb, Qpp, Qps, Vpp, Vps