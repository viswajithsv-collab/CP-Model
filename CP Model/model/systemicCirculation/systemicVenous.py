def splanchicVenous(Psvb, Psv, Pra, Ptv, dVusv, Rsvb, Rsv, Rtv, Csv, Vusvs, P_abd=0):
    """Splanchnic venous (A8, A13, A14) with abdominal pressure reference"""
    # A8: Pressure derivative with abdominal pressure reference
    fin = (Psvb - Psv) / Rsvb
    f1 = ((Psv - P_abd) - Pra) / Rsv  # Modified for abdominal pressure
    f2 = dVusv  # Unstressed volume change
    fout = f1 + f2
    dPsv = (fin - fout) / Csv

    # A13: Flow to thoracic veins
    Qsv = ((Psv - P_abd) - Ptv) / Rtv

    # A14: Venous volume
    Vsv = Csv * (Psv - P_abd) + Vusvs

    return dPsv, Qsv, Vsv


def activeMuscleVeins(Psvb, Pamv, Pra, Ptv, dVuamv, Ramvb, Ramv, Rtv, Camv, Vuamvs, P_im=0, exercise_mode=False,
                      k_ram=24.17):
    """Active muscle venous (A9, A13, A14) with muscle pump effects"""

    # Calculate effective venous resistance based on exercise mode
    if exercise_mode and P_im > 0:
        # During exercise: resistance inversely proportional to volume (Equation 12)
        V_estimate = Camv * (Pamv - P_im) + Vuamvs
        Ramv_effective = k_ram / max(V_estimate, 0.1 * Vuamvs)  # Prevent division by zero
    else:
        # At rest: normal Starling resistor behavior
        Ramv_effective = Ramv

    # A9: Pressure derivative with intramuscular pressure
    fin = (Psvb - Pamv) / Ramvb
    f1 = ((Pamv - P_im) - Pra) / Ramv_effective  # Modified for intramuscular pressure
    f2 = dVuamv  # Unstressed volume change
    fout = f1 + f2
    dPamv = (fin - fout) / Camv

    # A13: Flow to thoracic veins with muscle pump
    Qamv = ((Pamv - P_im) - Ptv) / Rtv

    # A14: Venous volume with intramuscular pressure
    Vamv = Camv * (Pamv - P_im) + Vuamvs

    return dPamv, Qamv, Vamv, Ramv_effective


def restingMuscleVeins(Psvb, Prmv, Pra, Ptv, dVurmv, Rrmvb, Rrmv, Rtv, Crmv, Vurmvs):
    """Resting muscle venous (A9 variant, A13, A14) - NO muscle pump effects"""

    # A9: Pressure derivative (normal Starling resistor)
    fin = (Psvb - Prmv) / Rrmvb
    f1 = (Prmv - Pra) / Rrmv  # No intramuscular pressure for resting muscle
    f2 = dVurmv  # Unstressed volume change
    fout = f1 + f2
    dPrmv = (fin - fout) / Crmv

    # A13: Flow to thoracic veins
    Qrmv = (Prmv - Ptv) / Rtv

    # A14: Venous volume
    Vrmv = Crmv * Prmv + Vurmvs

    return dPrmv, Qrmv, Vrmv


def brainVeins(Psvb, Pbv, Pra, Ptv, Rbp, Rbv, Rtv, Cbv, Vubvs, P_thor=0):
    """Brain venous (A10, A13, A14) with thoracic pressure reference"""
    # A10: Pressure derivative
    fin = (Psvb - Pbv) / Rbp
    fout = ((Pbv - P_thor) - Pra) / Rbv  # Modified for thoracic pressure
    dPbv = (fin - fout) / Cbv

    # A13: Flow to thoracic veins
    Qbv = ((Pbv - P_thor) - Ptv) / Rtv

    # A14: Venous volume
    Vbv = Cbv * (Pbv - P_thor) + Vubvs

    return dPbv, Qbv, Vbv


def coronaryVeins(Psvb, Phv, Pra, Ptv, Rhp, Rhv, Rtv, Chv, Vuhvs, P_thor=0):
    """Coronary venous (A11, A13, A14) with thoracic pressure reference"""
    # A11: Pressure derivative
    fin = (Psvb - Phv) / Rhp
    fout = ((Phv - P_thor) - Pra) / Rhv  # Modified for thoracic pressure
    dPhv = (fin - fout) / Chv

    # A13: Flow to thoracic veins
    Qhv = ((Phv - P_thor) - Ptv) / Rtv

    # A14: Venous volume
    Vhv = Chv * (Phv - P_thor) + Vuhvs

    return dPhv, Qhv, Vhv


def extrasplanchicVenous(TBV, Vnet, Ptv, Cev, Rtv, Vuevs, P_thor=0):
    """Extrasplanchnic venous - volume conservation (A12, A13, A14) with thoracic pressure"""
    # A12: Volume conservation (now accounts for 6 compartments)
    Pev = (TBV - Vnet) / Cev

    # A13: Flow to thoracic veins
    Qev = ((Pev - P_thor) - Ptv) / Rtv

    # A14: Venous volume
    Vev = Cev * (Pev - P_thor) + Vuevs

    return Pev, Qev, Vev