# parameters.py
# Albanese 2016 Cardiovascular Model Parameters
# Edit these values freely to simulate different physiological conditions

ALBANESE_PARAMS = {
    # ============================================
    # SYSTEMIC ARTERY
    # ============================================
    'Rsa': 0.06,      # Systemic arterial resistance [mmHg·s/mL] (69)
    'Lsa': 0.18e-3,   # Systemic arterial inertance [mmHg·s²/mL] (69)
    'Csa': 0.28,      # Systemic arterial compliance [mL/mmHg] (69)
    'Vusa': 0,        # Systemic arterial unstressed volume [mL] (69)
    
    # ============================================
    # PERIPHERAL COMPARTMENTS
    # ============================================
    # Splanchnic
    'Rsp': 2.49,      # Splanchnic peripheral resistance [mmHg·s/mL] (69)
    'Csp': 1.533,     # Splanchnic peripheral compliance [mL/mmHg] [MODEL]
    'Vusp': 274.4,    # Splanchnic peripheral unstressed volume [mL] (69)
    
    # Extrasplanchnic
    'Rep': 1.665,     # Extrasplanchnic peripheral resistance [mmHg·s/mL] (69)
    'Cep': 1.0758,    # Extrasplanchnic peripheral compliance [mL/mmHg] [MODEL]
    'Vuep': 134.64,   # Extrasplanchnic peripheral unstressed volume [mL] (69)
    
    # Muscle
    'Rmp': 2.106,     # Muscle peripheral resistance [mmHg·s/mL] (69)
    'Cmp': 0.8184,    # Muscle peripheral compliance [mL/mmHg] [MODEL]
    'Vump': 105.8,    # Muscle peripheral unstressed volume [mL] (69)
    
    # Brain
    'Rbp': 19.71,     # Brain peripheral resistance [mmHg·s/mL] (69)
    'Cbp': 0.1488,    # Brain peripheral compliance [mL/mmHg] [MODEL]
    'Vubp': 24,       # Brain peripheral unstressed volume [mL] (69)
    
    # Coronary (Heart)
    'Rhp': 4.08,      # Coronary peripheral resistance [mmHg·s/mL] (69)
    'Chp': 0.1,       # Coronary peripheral compliance [mL/mmHg] (69)
    'Vuhp': 20,       # Coronary peripheral unstressed volume [mL] (69)
    
    # ============================================
    # VENOUS COMPARTMENTS
    # ============================================
    # Splanchnic venous
    'Rsv': 0.038,     # Splanchnic venous resistance (to RA) [mmHg·s/mL] (69)
    'Csv': 42.777,    # Splanchnic venous compliance [mL/mmHg] [MODEL]
    'Vusv': 1435.4,   # Splanchnic venous unstressed volume [mL] (69)
    
    # Muscle venous
    'Rmv': 0.034,     # Muscle venous resistance (to RA) [mmHg·s/mL] (69)
    'Cmv': 14,        # Muscle venous compliance [mL/mmHg] [MODEL]
    'Vumv': 640.73,   # Muscle venous unstressed volume [mL] (69)
    
    # Brain venous
    'Rbv': 0.214,     # Brain venous resistance (to RA) [mmHg·s/mL] (69)
    'Cbv': 1.017,     # Brain venous compliance [mL/mmHg] [MODEL]
    'Vubv': 109.21,   # Brain venous unstressed volume [mL] (69)
    
    # Coronary venous
    'Rhv': 0.0234,    # Coronary venous resistance (to RA) [mmHg·s/mL] (69)
    'Chv': 1.859,     # Coronary venous compliance [mL/mmHg] [MODEL]
    'Vuhv': 98.21,    # Coronary venous unstressed volume [mL] (69)
    
    # Extrasplanchnic venous (volume conservation)
    'Cev': 7.497,     # Extrasplanchnic venous compliance [mL/mmHg] [MODEL]
    'Vuev': 294.64,   # Extrasplanchnic venous unstressed volume [mL] (69)
    
    # ============================================
    # THORACIC VEINS
    # ============================================
    # Nonlinear P-V parameters (Equation 2 - Table 2)
    'D1': 0.385,      # Upper branch offset [mmHg] (9)
    'K1': 0.15,       # Upper branch slope [mmHg/mL] (9)
    'Vutv': 130,      # Thoracic veins unstressed volume [mL] (9)
    'D2': -5,         # Lower branch offset [mmHg] (49)
    'K2': 2,          # Lower branch exponential coefficient [mmHg] (49)
    'Vtv_min': 130,   # Lower branch volume scale [mL] (9)
    'K_xp': 0.001,    # Correction term numerator [mmHg] (9)
    'K_xv': 350,      # Correction term denominator [mL] (9)
    
    # Variable resistance parameters (Equation 3 - Table 2)
    'KR': 0.025,      # Resistance scaling factor [mmHg·s·mL] (9)
    'Vtv_max': 350,   # Maximum thoracic veins volume [mL] (9)
    'Rtv_0': 0.025,   # Offset resistance [mmHg·s/mL] (9)
    
    # Resistance to thoracic veins (same for all venous beds)
    'Rtv': 0.023,     # Resistance to thoracic veins [mmHg·s/mL] (69)
    
    # ============================================
    # GLOBAL PARAMETERS
    # ============================================
    'TBV': 5300,      # Total blood volume [mL]
    'Vtv_init': 200,  # Initial thoracic veins volume [mL] - typical value
}