def restingMuscleVenous(Qrmp, Prmv, Pra, Ptv, dVurmv, Rrmv, Rtv, Crmv, Vurmv):
    """
    Resting muscle venous compartment - Standard Albanese (linear P-V)
    
    Albanese equations A9, A13, A14 for resting muscle (j=rmp):
    - A9: Venous pressure derivative (Starling resistor)
    - A13: Flow to thoracic veins
    - A14: Venous volume
    
    Note: NO intramuscular pressure (Pim = 0)
    Note: NO nonlinear P-V (standard linear compliance)
    Note: Used for muscle beds NOT undergoing exercise
    
    Parameters:
    - Qrmp: inflow from resting muscle peripheral
    - Prmv: resting muscle venous pressure
    - Pra: right atrial pressure
    - Ptv: thoracic venous pressure
    - dVurmv: rate of unstressed volume change
    - Rrmv: resting muscle venous resistance (to RA)
    - Rtv: resistance to thoracic veins
    - Crmv: resting muscle venous compliance
    - Vurmv: resting muscle venous unstressed volume
    
    Returns:
    - dPrmv: pressure derivative (for RK45 integration)
    - Qrmv: flow to thoracic veins
    - Vrmv: resting muscle venous volume
    """
    # A9: Pressure derivative (Starling resistor)
    fin = Qrmp
    fout_ra = (Prmv - Pra) / Rrmv
    fout_unstressed = dVurmv
    fout = fout_ra + fout_unstressed
    dPrmv = (fin - fout) / Crmv
    
    # A13: Flow to thoracic veins
    Qrmv = (Prmv - Ptv) / Rtv
    
    # A14: Venous volume (linear P-V)
    Vrmv = Crmv * Prmv + Vurmv
    
    return dPrmv, Qrmv, Vrmv
