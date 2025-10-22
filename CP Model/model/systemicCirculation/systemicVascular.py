def systemicVascular(Psvb, Psa, Psv, Pev, Pamv, Prmv, Pbv, Phv, Rsa, Rsvb, Revb, Ramvb, Rrmvb, Rbvb, Rhvb,
                     Csvb, Cevb, Camvb, Crmvb, Cbvb, Chvb, Vusvb, Vuevb, Vuamvb, Vurmvb, Vubvb, Vuhvb):
    """
    Systemic vascular (peripheral distribution) - 6 COMPARTMENTS like Ursino 2002
    Compartments: splanchnic, extrasplanchnic, active muscle, resting muscle, brain, heart

    Returns:
    - dPsvb: pressure derivative
    - Individual flows: Qsv, Qev, Qamv, Qrmv, Qbv, Qhv
    - Individual volumes: Vsvb, Vevb, Vamvb, Vrmvb, Vbvb, Vhvb
    - Fin: inflow from systemic arteries
    """
    # Inflow from systemic arteries
    Fin = (Psa - Psvb) / Rsa

    # Individual outflows to 6 peripheral beds (A6)
    Qsv = (Psvb - Psv) / Rsvb  # Splanchnic flow
    Qev = (Psvb - Pev) / Revb  # Extrasplanchnic flow
    Qamv = (Psvb - Pamv) / Ramvb  # Active muscle flow (leg muscles)
    Qrmv = (Psvb - Prmv) / Rrmvb  # Resting muscle flow (other muscles)
    Qbv = (Psvb - Pbv) / Rbvb  # Brain flow
    Qhv = (Psvb - Phv) / Rhvb  # Heart flow

    # Individual volumes (A7)
    Vsvb = Csvb * Psvb + Vusvb  # Splanchnic volume
    Vevb = Cevb * Psvb + Vuevb  # Extrasplanchnic volume
    Vamvb = Camvb * Psvb + Vuamvb  # Active muscle volume
    Vrmvb = Crmvb * Psvb + Vurmvb  # Resting muscle volume
    Vbvb = Cbvb * Psvb + Vubvb  # Brain volume
    Vhvb = Chvb * Psvb + Vuhvb  # Heart volume

    # Total outflow
    Fout = Qsv + Qev + Qamv + Qrmv + Qbv + Qhv

    # Total compliance (A4)
    Ctot = Csvb + Cevb + Camvb + Crmvb + Cbvb + Chvb

    # Pressure derivative (A4)
    dPsvb = (Fin - Fout) / Ctot

    return dPsvb, Qsv, Qev, Qamv, Qrmv, Qbv, Qhv, Vsvb, Vevb, Vamvb, Vrmvb, Vbvb, Vhvb, Fin