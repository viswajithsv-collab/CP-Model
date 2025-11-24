def activeMusclePeripheral(Pep, Pamv, Ramp, Camp, Vuamp):
    """
    Active muscle peripheral compartment (arterial side) - Magosso extension
    
    Albanese equations A6-A7 adapted for active muscle (j=amp):
    - A6: Flow through peripheral resistance
    - A7: Volume calculation
    
    Note: Pep is the common equivalent peripheral pressure (equation A5).
    The pressure derivative dPep is calculated in extrasplanchnicPeripheral.py.
    
    Parameters:
    - Pep: equivalent peripheral pressure (common to all beds)
    - Pamv: active muscle venous pressure
    - Ramp: active muscle peripheral resistance
    - Camp: active muscle peripheral compliance
    - Vuamp: active muscle peripheral unstressed volume
    
    Returns:
    - Qamp: active muscle peripheral flow (to venous side)
    - Vamp: active muscle peripheral volume
    """
    # A6: Flow through active muscle peripheral bed
    Qamp = (Pep - Pamv) / Ramp
    
    # A7: Volume
    Vamp = Camp * Pep + Vuamp
    
    return Qamp, Vamp
