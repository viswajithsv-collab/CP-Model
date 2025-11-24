def coronaryPeripheral(Pep, Phv, Rhp, Chp, Vuhp):
    """
    Coronary (heart) peripheral compartment (arterial side)
    
    Albanese equations A6-A7 for j=h (heart/coronary):
    - A6: Flow through peripheral resistance
    - A7: Volume calculation
    
    Note: Pep is the common equivalent peripheral pressure (equation A5).
    The pressure derivative dPep is calculated in extrasplanchnicPeripheral.py.
    
    Parameters:
    - Pep: equivalent peripheral pressure (common to all beds)
    - Phv: coronary venous pressure
    - Rhp: coronary peripheral resistance
    - Chp: coronary peripheral compliance
    - Vuhp: coronary peripheral unstressed volume
    
    Returns:
    - Qhp: coronary peripheral flow (to venous side)
    - Vhp: coronary peripheral volume
    """
    # A6: Flow through coronary peripheral bed
    Qhp = (Pep - Phv) / Rhp
    
    # A7: Volume
    Vhp = Chp * Pep + Vuhp
    
    return Qhp, Vhp
