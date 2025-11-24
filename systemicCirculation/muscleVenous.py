def muscleVenous(Qmp, Pmv, Pra, Ptv, dVumv, Rmv, Rtv, Cmv, Vumv):
    """
    Muscle venous compartment
    
    Albanese equations A9, A13, A14 for j=m (muscle):
    - A9: Venous pressure derivative (Starling resistor)
    - A13: Flow to thoracic veins
    - A14: Venous volume
    
    Note: NO pressure references (P_im = 0 for Albanese)
    Note: NO muscle pump effects (rest/supine condition only)
    
    Parameters:
    - Qmp: inflow from muscle peripheral
    - Pmv: muscle venous pressure
    - Pra: right atrial pressure
    - Ptv: thoracic venous pressure
    - dVumv: rate of unstressed volume change
    - Rmv: muscle venous resistance (to RA)
    - Rtv: resistance to thoracic veins
    - Cmv: muscle venous compliance
    - Vumv: muscle venous unstressed volume
    
    Returns:
    - dPmv: pressure derivative (for RK45 integration)
    - Qmv: flow to thoracic veins
    - Vmv: muscle venous volume
    """
    # A9: Pressure derivative (Starling resistor)
    fin = Qmp
    fout_ra = (Pmv - Pra) / Rmv
    fout_unstressed = dVumv
    fout = fout_ra + fout_unstressed
    dPmv = (fin - fout) / Cmv
    
    # A13: Flow to thoracic veins
    Qmv = (Pmv - Ptv) / Rtv
    
    # A14: Venous volume
    Vmv = Cmv * Pmv + Vumv
    
    return dPmv, Qmv, Vmv
