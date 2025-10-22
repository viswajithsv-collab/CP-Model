def pulmonaryVeins(Qpp, Qps, Ppv, Pla, Rpv, Cpv, Vu_pv=0, P_thor=0, dP_thor=0):
    """
    Pulmonary veins with optional intrathoracic pressure reference (A27-A29)

    Based on:
    - A27: Cpv * d(Ppv - P_thor)/dt = Qpp + Qps - Qpv
    - A28: Qpv = (Ppv - Pla)/Rpv
    - A29: Vpv = Cpv * (Ppv - P_thor) + Vu,pv

    Optional parameters (default to 0 for non-exercise simulations):
    - Vu_pv: unstressed volume [default: 0]
    - P_thor: intrathoracic pressure (mmHg) [default: 0]
    - dP_thor: intrathoracic pressure derivative (mmHg/s) [default: 0]
    """
    # A27: Total inflow (peripheral + shunt)
    Fin = Qpp + Qps

    # A28: Outflow to left atrium
    Qpv = (Ppv - Pla) / Rpv

    # A27: Pressure derivative with optional intrathoracic reference
    # Cpv * d(Ppv - P_thor)/dt = Fin - Qpv
    # Cpv * (dPpv - dP_thor) = Fin - Qpv
    # dPpv = (Fin - Qpv)/Cpv + dP_thor
    # When dP_thor=0, reduces to original equation
    dPpv = (Fin - Qpv) / Cpv + dP_thor

    # A29: Volume with optional intrathoracic reference
    # When P_thor=0, reduces to original equation
    Vpv = Cpv * (Ppv - P_thor) + Vu_pv

    return dPpv, Qpv, Vpv