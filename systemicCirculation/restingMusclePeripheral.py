def restingMusclePeripheral(Pep, Prmv, Rrmp, Crmp, Vurmp):
    """
    Resting muscle peripheral compartment (arterial side) - Magosso extension
    
    Albanese equations A6-A7 adapted for resting muscle (j=rmp):
    - A6: Flow through peripheral resistance
    - A7: Volume calculation
    
    Note: Pep is the common equivalent peripheral pressure (equation A5).
    The pressure derivative dPep is calculated in extrasplanchnicPeripheral.py.
    
    Parameters:
    - Pep: equivalent peripheral pressure (common to all beds)
    - Prmv: resting muscle venous pressure
    - Rrmp: resting muscle peripheral resistance
    - Crmp: resting muscle peripheral compliance
    - Vurmp: resting muscle peripheral unstressed volume
    
    Returns:
    - Qrmp: resting muscle peripheral flow (to venous side)
    - Vrmp: resting muscle peripheral volume
    """
    # A6: Flow through resting muscle peripheral bed
    Qrmp = (Pep - Prmv) / Rrmp
    
    # A7: Volume
    Vrmp = Crmp * Pep + Vurmp
    
    return Qrmp, Vrmp
