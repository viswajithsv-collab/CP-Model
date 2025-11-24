def brainPeripheral(Pep, Pbv, Rbp, Cbp, Vubp):
    """
    Brain peripheral compartment (arterial side)
    
    Albanese equations A6-A7 for j=b (brain):
    - A6: Flow through peripheral resistance
    - A7: Volume calculation
    
    Note: Pep is the common equivalent peripheral pressure (equation A5).
    The pressure derivative dPep is calculated in extrasplanchnicPeripheral.py.
    
    Parameters:
    - Pep: equivalent peripheral pressure (common to all beds)
    - Pbv: brain venous pressure
    - Rbp: brain peripheral resistance
    - Cbp: brain peripheral compliance
    - Vubp: brain peripheral unstressed volume
    
    Returns:
    - Qbp: brain peripheral flow (to venous side)
    - Vbp: brain peripheral volume
    """
    # A6: Flow through brain peripheral bed
    Qbp = (Pep - Pbv) / Rbp
    
    # A7: Volume
    Vbp = Cbp * Pep + Vubp
    
    return Qbp, Vbp
