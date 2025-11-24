def brainVenous(Qbp, Pbv, Pra, Ptv, Rbv, Rtv, Cbv, Vubv):
    """
    Brain venous compartment
    
    Albanese equations A10, A13, A14 for j=b (brain):
    - A10: Venous pressure derivative (Starling resistor)
    - A13: Flow to thoracic veins
    - A14: Venous volume
    
    Note: NO pressure references (P_thor = 0 for Albanese)
    
    Parameters:
    - Qbp: inflow from brain peripheral
    - Pbv: brain venous pressure
    - Pra: right atrial pressure
    - Ptv: thoracic venous pressure
    - Rbv: brain venous resistance (to RA)
    - Rtv: resistance to thoracic veins
    - Cbv: brain venous compliance
    - Vubv: brain venous unstressed volume
    
    Returns:
    - dPbv: pressure derivative (for RK45 integration)
    - Qbv: flow to thoracic veins
    - Vbv: brain venous volume
    """
    # A10: Pressure derivative (Starling resistor)
    fin = Qbp
    fout_ra = (Pbv - Pra) / Rbv
    dPbv = (fin - fout_ra) / Cbv
    
    # A13: Flow to thoracic veins
    Qbv = (Pbv - Ptv) / Rtv
    
    # A14: Venous volume
    Vbv = Cbv * Pbv + Vubv
    
    return dPbv, Qbv, Vbv
