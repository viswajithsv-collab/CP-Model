def extrasplanchnicVenous(TBV, Vnet, Ptv, Rtv, Cev, Vuev):
    """
    Extrasplanchnic venous compartment (volume conservation)
    
    Albanese equations A12, A13, A14 for j=e (extrasplanchnic):
    - A12: Pressure from volume conservation
    - A13: Flow to thoracic veins
    - A14: Venous volume
    
    Note: Extrasplanchnic venous acts as the volume buffer to ensure
    total blood volume conservation. Its pressure is determined by
    the remaining volume after accounting for all other compartments.
    
    Parameters:
    - TBV: total blood volume
    - Vnet: sum of all volumes in OTHER compartments
    - Ptv: thoracic venous pressure
    - Rtv: resistance to thoracic veins
    - Cev: extrasplanchnic venous compliance
    - Vuev: extrasplanchnic venous unstressed volume
    
    Returns:
    - Pev: extrasplanchnic venous pressure
    - Qev: flow to thoracic veins
    - Vev: extrasplanchnic venous volume
    """
    # A12: Volume conservation (Vev = TBV - Vnet)
    Vev = TBV - Vnet
    
    # Pressure from volume
    Pev = (Vev - Vuev) / Cev
    
    # A13: Flow to thoracic veins
    Qev = (Pev - Ptv) / Rtv
    
    return Pev, Qev, Vev
