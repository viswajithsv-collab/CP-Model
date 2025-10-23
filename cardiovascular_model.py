"""
Cardiovascular Model - Python Implementation
Based on Ursino 1998 simplified model
Converted from MATLAB by Claude
"""

import numpy as np
from typing import Tuple


class CardiovascularParameters:
    """Store all cardiovascular model parameters"""
    
    def __init__(self):
        # Compliance Constants (ml/mmHg)
        self.Csa = 0.28
        self.Clbp = 2.05
        self.Cubp = 1.67
        self.Clbv = 61.11
        self.Cubv = 50.0
        self.Cpa = 0.76
        self.Cpp = 5.80
        self.Cpv = 25.37
        
        # Resistance Constants (mmHg.s/ml)
        self.Rsa = 0.06
        self.Rlbp = 1.307
        self.Rubp = 1.407
        self.Rlbv = 0.038
        self.Rubv = 0.016
        self.Rpa = 0.023
        self.Rpp = 0.0894
        self.Rpv = 0.0056
        
        # Unstressed Volume Constants (ml)
        self.Vusa = 0
        self.Vulbp = 274.4
        self.Vuubp = 336.6
        self.Vulbv = 1121
        self.Vuubv = 1375
        self.Vupa = 0
        self.Vupp = 223
        self.Vupv = 120
        
        # Total Blood Volume (ml)
        self.TBV = 5300
        
        # Left Heart
        self.Cla = 19.23
        self.Vula = 25
        self.Rla = 2.5e-3
        self.Vulv = 16.77
        
        # Right Heart
        self.Cra = 31.25
        self.Vura = 25
        self.Rra = 2.5e-3
        self.Vurv = 40.8
        
        # Valve Resistances
        self.Raov = 0.0025
        self.Rmv = 0
        self.Rtv = 0
        self.Rpulv = 0.0025


class CardiovascularState:
    """Store cardiovascular state variables"""
    
    def __init__(self):
        # Pressures (mmHg)
        self.Ppv = 2.0
        self.Ppp = 2.0
        self.Ppa = 5.0
        self.Psa = 60.0
        self.Plbp = 10.0
        self.Plbv = 10.0
        self.Pubv = 9.0
        self.LAP = 6.0
        self.LVP = 5.0
        self.RAP = 5.0
        self.RVP = 5.0
        
        # Volumes (ml)
        self.LVV = 120.0
        self.RVV = 120.0
        
        # Flows (ml/s)
        self.Qmv = 1.0
        self.Qaov = 1.0
        self.Qpulv = 1.0
        self.Qtv = 1.0


def phi1(t: np.ndarray, HR: float, alpha: list, n: list) -> np.ndarray:
    """
    Double-Hill activation function for ventricular contraction
    
    Parameters:
    -----------
    t : array
        Time vector
    HR : float
        Heart rate (bpm)
    alpha : list
        [alpha1, alpha2] time constants
    n : list
        [n1, n2] exponents
    
    Returns:
    --------
    En : array
        Normalized elastance function
    """
    Tc = 60.0 / HR
    tm = np.mod(t, Tc)
    x = tm / Tc
    
    a1 = x / alpha[0]
    a2 = x / alpha[1]
    
    m = a1 ** n[0]
    o = a2 ** n[1]
    
    p = m / (1 + m)
    q = 1 / (1 + o)
    
    z = p * q
    mEn = np.max(z)
    
    En = z / mEn
    return En


def valves(Pin: float, Pout: float, R: float) -> float:
    """
    Calculate flow through heart valve
    
    Parameters:
    -----------
    Pin : float
        Inlet pressure (mmHg)
    Pout : float
        Outlet pressure (mmHg)
    R : float
        Valve resistance (mmHg.s/ml)
    
    Returns:
    --------
    F : float
        Flow rate (ml/s)
    """
    if Pin <= Pout:
        return 0.0
    else:
        return (Pin - Pout) / R


def ventricle(Emax: float, Emin: float, E: float, Vold: float, 
              Vu: float, Fin: float, Fout: float, h: float) -> Tuple[float, float]:
    """
    Ventricular dynamics (time-varying elastance model)
    
    Parameters:
    -----------
    Emax : float
        Maximum elastance (mmHg/ml)
    Emin : float
        Minimum elastance (mmHg/ml)
    E : float
        Current activation level (0-1)
    Vold : float
        Previous volume (ml)
    Vu : float
        Unstressed volume (ml)
    Fin : float
        Inflow (ml/s)
    Fout : float
        Outflow (ml/s)
    h : float
        Time step (s)
    
    Returns:
    --------
    V : float
        New volume (ml)
    P : float
        Ventricular pressure (mmHg)
    """
    V = Vold + (Fin - Fout) * h
    ESP = Emax * (V - Vu)
    EDP = Emin * (V - Vu)
    P = E * ESP + (1 - E) * EDP
    return V, P


def left_atrium(Ppv: float, LAP: float, Rpv: float, Fmv: float, Cla: float) -> float:
    """Left atrium pressure dynamics"""
    Fin = (Ppv - LAP) / Rpv
    dPla = (Fin - Fmv) / Cla
    return dPla


def right_atrium(Plbv: float, Pubv: float, RAP: float, 
                 Rlbv: float, Rubv: float, Ftv: float, Cra: float) -> float:
    """Right atrium pressure dynamics"""
    Fin = (Plbv - RAP) / Rlbv + (Pubv - RAP) / Rubv
    dPra = (Fin - Ftv) / Cra
    return dPra


def systemic_artery_RC(Fin: float, Psa: float, Psp: float, 
                       Rsa: float, Csa: float) -> float:
    """Systemic arterial pressure dynamics"""
    dPsa = (Fin - (Psa - Psp) / Rsa) / Csa
    return dPsa


def systemic_peripheral_RC(Psa: float, Plbp: float, Plbv: float, Pubv: float,
                           Rsa: float, Rlbp: float, Rubp: float, 
                           Clbp: float, Cubp: float) -> float:
    """Systemic peripheral pressure dynamics"""
    f1 = (Plbp - Plbv) / Rlbp
    f2 = (Plbp - Pubv) / Rubp
    Fout = f1 + f2
    Fin = (Psa - Plbp) / Rsa
    dPlbp = (Fin - Fout) / (Clbp + Cubp)
    return dPlbp


def extrasplanchnic_venous(Psp: float, Pev: float, Pra: float, 
                           dVuev: float, Rep: float, Rev: float, Cev: float) -> float:
    """Extrasplanchnic venous pressure dynamics"""
    Fin = (Psp - Pev) / Rep
    f1 = (Pev - Pra) / Rev
    Fout = f1 + dVuev
    dPev = (Fin - Fout) / Cev
    return dPev


def pulmonary_artery_RC(Fin: float, Ppa: float, Ppp: float, 
                        Rpa: float, Cpa: float) -> float:
    """Pulmonary arterial pressure dynamics"""
    Fout = (Ppa - Ppp) / Rpa
    dPpa = (Fin - Fout) / Cpa
    return dPpa


def pulmonary_peripheral_RC(Ppa: float, Ppp: float, Ppv: float,
                            Rpa: float, Rpp: float, Cpp: float) -> float:
    """Pulmonary peripheral pressure dynamics"""
    Fin = (Ppa - Ppp) / Rpa
    Fout = (Ppp - Ppv) / Rpp
    dPpp = (Fin - Fout) / Cpp
    return dPpp


def pulmonary_veins(Ppp: float, Ppv: float, Pla: float,
                    Rpp: float, Rpv: float, Cpv: float) -> float:
    """Pulmonary venous pressure dynamics"""
    Fin = (Ppp - Ppv) / Rpp
    Fout = (Ppv - Pla) / Rpv
    dPpv = (Fin - Fout) / Cpv
    return dPpv


def splanchnic_venous(TBV: float, Vsv: float, Csv: float) -> float:
    """Splanchnic venous pressure"""
    Psv = (TBV - Vsv) / Csv
    return Psv


def simulate_cardiovascular_system(params: CardiovascularParameters, 
                                   state: CardiovascularState,
                                   HR: float = 75.0,
                                   duration: float = 16.0,
                                   dt: float = 0.0001,
                                   Emaxlv: float = 2.7,
                                   Eminlv: float = 0.06,
                                   Emaxrv: float = 1.6,
                                   Eminrv: float = 0.08) -> dict:
    """
    Run cardiovascular simulation
    
    Parameters:
    -----------
    params : CardiovascularParameters
        Model parameters
    state : CardiovascularState
        Initial state
    HR : float
        Heart rate (bpm)
    duration : float
        Simulation duration (s)
    dt : float
        Time step (s)
    
    Returns:
    --------
    results : dict
        Dictionary containing time series of all variables
    """
    # Time vector
    t = np.arange(0, duration, dt)
    n_steps = len(t)
    
    # Activation function parameters
    alpha = [0.103, 0.408]
    n = [1.9, 21.9]
    E = phi1(t, HR, alpha, n)
    
    # Ventricular elastances from parameters (not hardcoded!)
    # Emaxlv, Eminlv, Emaxrv, Eminrv are now function parameters
    
    # Initialize arrays
    results = {
        'time': t,
        'LAP': np.zeros(n_steps),
        'RAP': np.zeros(n_steps),
        'LVV': np.zeros(n_steps),
        'LVP': np.zeros(n_steps),
        'RVV': np.zeros(n_steps),
        'RVP': np.zeros(n_steps),
        'Psa': np.zeros(n_steps),
        'Plbp': np.zeros(n_steps),
        'Plbv': np.zeros(n_steps),
        'Pubv': np.zeros(n_steps),
        'Ppa': np.zeros(n_steps),
        'Ppp': np.zeros(n_steps),
        'Ppv': np.zeros(n_steps),
        'Qmv': np.zeros(n_steps),
        'Qaov': np.zeros(n_steps),
        'Qtv': np.zeros(n_steps),
        'Qpulv': np.zeros(n_steps),
        'Vu': np.zeros(n_steps),
        'Vlbv': np.zeros(n_steps)
    }
    
    # Set initial conditions
    results['LAP'][0] = state.LAP
    results['RAP'][0] = state.RAP
    results['LVV'][0] = state.LVV
    results['LVP'][0] = state.LVP
    results['RVV'][0] = state.RVV
    results['RVP'][0] = state.RVP
    results['Psa'][0] = state.Psa
    results['Plbp'][0] = state.Plbp
    results['Plbv'][0] = state.Plbv
    results['Pubv'][0] = state.Pubv
    results['Ppa'][0] = state.Ppa
    results['Ppp'][0] = state.Ppp
    results['Ppv'][0] = state.Ppv
    results['Qmv'][0] = state.Qmv
    results['Qaov'][0] = state.Qaov
    results['Qtv'][0] = state.Qtv
    results['Qpulv'][0] = state.Qpulv
    
    # Time integration
    for i in range(n_steps - 1):
        # Left Atrium
        dPla = left_atrium(results['Ppv'][i], results['LAP'][i], 
                          params.Rpv, results['Qmv'][i], params.Cla)
        results['LAP'][i+1] = results['LAP'][i] + dPla * dt
        
        # Right Atrium
        dPra = right_atrium(results['Plbv'][i], results['Pubv'][i], results['RAP'][i],
                           params.Rlbv, params.Rubv, results['Qtv'][i], params.Cra)
        results['RAP'][i+1] = results['RAP'][i] + dPra * dt
        
        # Left Ventricle
        results['LVV'][i+1], results['LVP'][i+1] = ventricle(
            Emaxlv, Eminlv, E[i], results['LVV'][i], params.Vulv,
            results['Qmv'][i], results['Qaov'][i], dt
        )
        
        # Right Ventricle
        results['RVV'][i+1], results['RVP'][i+1] = ventricle(
            Emaxrv, Eminrv, E[i], results['RVV'][i], params.Vurv,
            results['Qtv'][i], results['Qpulv'][i], dt
        )
        
        # Systemic Artery Circulation
        dPsa = systemic_artery_RC(results['Qaov'][i], results['Psa'][i], 
                                  results['Plbp'][i], params.Rsa, params.Csa)
        results['Psa'][i+1] = results['Psa'][i] + dPsa * dt
        
        # Lower Body Peripheral Circulation
        dPlbp = systemic_peripheral_RC(
            results['Psa'][i], results['Plbp'][i], results['Plbv'][i], results['Pubv'][i],
            params.Rsa, params.Rlbp, params.Rubp, params.Clbp, params.Cubp
        )
        results['Plbp'][i+1] = results['Plbp'][i] + dPlbp * dt
        
        # Upper Body Venous
        dPubv = extrasplanchnic_venous(
            results['Plbp'][i], results['Pubv'][i], results['RAP'][i],
            0, params.Rubp, params.Rubv, params.Cubv
        )
        results['Pubv'][i+1] = results['Pubv'][i] + dPubv * dt
        
        # Pulmonary Circulation
        dPpa = pulmonary_artery_RC(results['Qpulv'][i], results['Ppa'][i],
                                   results['Ppp'][i], params.Rpa, params.Cpa)
        results['Ppa'][i+1] = results['Ppa'][i] + dPpa * dt
        
        dPpp = pulmonary_peripheral_RC(results['Ppa'][i], results['Ppp'][i],
                                       results['Ppv'][i], params.Rpa, params.Rpp, params.Cpp)
        results['Ppp'][i+1] = results['Ppp'][i] + dPpp * dt
        
        dPpv = pulmonary_veins(results['Ppp'][i], results['Ppv'][i], results['LAP'][i],
                               params.Rpp, params.Rpv, params.Cpv)
        results['Ppv'][i+1] = results['Ppv'][i] + dPpv * dt
        
        # Unstressed Volume
        results['Vu'][i+1] = (params.Vusa + params.Vulbp + params.Vuubp + 
                             params.Vulbv + params.Vuubv + params.Vura + 
                             params.Vupa + params.Vupp + params.Vupv + params.Vula)
        
        # Splanchnic Venous Circulation
        results['Vlbv'][i+1] = (
            params.Csa * results['Psa'][i+1] + 
            (params.Clbp + params.Cubp) * results['Plbp'][i+1] +
            params.Cubv * results['Pubv'][i+1] + 
            params.Cra * results['RAP'][i+1] + 
            results['RVV'][i+1] + 
            params.Cpa * results['Ppa'][i+1] +
            params.Cpp * results['Ppp'][i+1] + 
            params.Cpv * results['Ppv'][i+1] +
            params.Cla * results['LAP'][i+1] + 
            results['LVV'][i+1] + 
            results['Vu'][i+1]
        )
        results['Plbv'][i+1] = splanchnic_venous(params.TBV, results['Vlbv'][i+1], params.Clbv)
        
        # Valves
        results['Qmv'][i+1] = valves(results['LAP'][i+1], results['LVP'][i+1], 
                                    params.Rla + params.Rmv)
        results['Qaov'][i+1] = valves(results['LVP'][i+1], results['Psa'][i+1], 
                                     params.Raov)
        results['Qtv'][i+1] = valves(results['RAP'][i+1], results['RVP'][i+1], 
                                    params.Rra + params.Rtv)
        results['Qpulv'][i+1] = valves(results['RVP'][i+1], results['Ppa'][i+1], 
                                      params.Rpulv)
    
    return results
