def splanchnicPeripheral(Pep, Psv, Rsp, Csp, Vusp):
    """
    Splanchnic peripheral compartment (arterial side)
    
    Albanese equations A6-A7 for j=s (splanchnic):
    - A6: Flow through peripheral resistance
    - A7: Volume calculation
    
    Note: Pep is the common equivalent peripheral pressure (equation A5).
    The pressure derivative dPep is calculated in extrasplanchnicPeripheral.py.
    
    Parameters:
    - Pep: equivalent peripheral pressure (common to all beds)
    - Psv: splanchnic venous pressure
    - Rsp: splanchnic peripheral resistance
    - Csp: splanchnic peripheral compliance
    - Vusp: splanchnic peripheral unstressed volume
    
    Returns:
    - Qsp: splanchnic peripheral flow (to venous side)
    - Vsp: splanchnic peripheral volume
    """
    # A6: Flow through splanchnic peripheral bed
    Qsp = (Pep - Psv) / Rsp
    
    # A7: Volume
    Vsp = Csp * Pep + Vusp
    
    return Qsp, Vsp
