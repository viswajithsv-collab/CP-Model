def coronaryVenous(Qhp, Phv, Pra, Ptv, Rhv, Rtv, Chv, Vuhv):
    """
    Coronary (heart) venous compartment
    
    Albanese equations A11, A13, A14 for j=h (heart/coronary):
    - A11: Venous pressure derivative (Starling resistor)
    - A13: Flow to thoracic veins
    - A14: Venous volume
    
    Note: NO pressure references (P_thor = 0 for Albanese)
    
    Parameters:
    - Qhp: inflow from coronary peripheral
    - Phv: coronary venous pressure
    - Pra: right atrial pressure
    - Ptv: thoracic venous pressure
    - Rhv: coronary venous resistance (to RA)
    - Rtv: resistance to thoracic veins
    - Chv: coronary venous compliance
    - Vuhv: coronary venous unstressed volume
    
    Returns:
    - dPhv: pressure derivative (for RK45 integration)
    - Qhv: flow to thoracic veins
    - Vhv: coronary venous volume
    """
    # A11: Pressure derivative (Starling resistor)
    fin = Qhp
    fout_ra = (Phv - Pra) / Rhv
    dPhv = (fin - fout_ra) / Chv
    
    # A13: Flow to thoracic veins
    Qhv = (Phv - Ptv) / Rtv
    
    # A14: Venous volume
    Vhv = Chv * Phv + Vuhv
    
    return dPhv, Qhv, Vhv
