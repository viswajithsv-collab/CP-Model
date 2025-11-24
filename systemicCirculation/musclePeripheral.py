def musclePeripheral(Pep, Pmv, Rmp, Cmp, Vump):
    """
    Muscle peripheral compartment (arterial side)
    
    Albanese equations A6-A7 for j=m (muscle):
    - A6: Flow through peripheral resistance
    - A7: Volume calculation
    
    Note: Pep is the common equivalent peripheral pressure (equation A5).
    The pressure derivative dPep is calculated in extrasplanchnicPeripheral.py.
    
    Parameters:
    - Pep: equivalent peripheral pressure (common to all beds)
    - Pmv: muscle venous pressure
    - Rmp: muscle peripheral resistance
    - Cmp: muscle peripheral compliance
    - Vump: muscle peripheral unstressed volume
    
    Returns:
    - Qmp: muscle peripheral flow (to venous side)
    - Vmp: muscle peripheral volume
    """
    # A6: Flow through muscle peripheral bed
    Qmp = (Pep - Pmv) / Rmp
    
    # A7: Volume
    Vmp = Cmp * Pep + Vump
    
    return Qmp, Vmp
