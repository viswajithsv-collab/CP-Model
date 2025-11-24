import numpy as np


def activeMuscleVenousNonlinear(Qamp, Vamv, Pamv, Pra, Ptv, Pim, dVuamv, 
                                 Ramv, Rtv, Camv, Vuamv, P0_amv):
    """
    Active muscle venous compartment with nonlinear P-V and muscle pump
    
    Magosso & Ursino 2002 Equation (1):
    - Nonlinear pressure-volume relationship for active muscle veins
    - Accounts for venous collapse during muscle contraction
    
    Albanese equations A9, A13 adapted for active muscle:
    - Volume derivative (instead of pressure derivative due to nonlinear P-V)
    - Flow to thoracic veins
    
    Parameters:
    - Qamp: inflow from active muscle peripheral
    - Vamv: active muscle venous volume (current)
    - Pamv: active muscle venous pressure (current)
    - Pra: right atrial pressure
    - Ptv: thoracic venous pressure
    - Pim: intramuscular pressure from muscle pump (Magosso Eq 2)
    - dVuamv: rate of unstressed volume change
    - Ramv: active muscle venous resistance (to RA)
    - Rtv: resistance to thoracic veins
    - Camv: active muscle venous compliance (for linear regime)
    - Vuamv: active muscle venous unstressed volume
    - P0_amv: nonlinear P-V parameter
    
    Returns:
    - dVamv: volume derivative (for RK45 integration)
    - Qamv: flow to thoracic veins
    - Pamv: active muscle venous pressure (computed from nonlinear P-V)
    """
    
    # Magosso Eq (1): Nonlinear P-V relationship
    if Vamv > Vuamv:
        # Linear regime (veins open)
        # Pamv - Pim = (1/Camv) * (Vamv - Vuamv)
        Pamv = Pim + (1.0 / Camv) * (Vamv - Vuamv)
    else:
        # Nonlinear regime (veins collapsed)
        # Pamv - Pim = P0 * [1 - (Vamv/Vuamv)^(-3/2)]
        Pamv = Pim + P0_amv * (1.0 - (Vamv / Vuamv) ** (-3.0 / 2.0))
    
    # A9 adapted: Volume derivative (Starling resistor)
    fin = Qamp
    fout_ra = (Pamv - Pra) / Ramv
    fout_unstressed = dVuamv
    fout = fout_ra + fout_unstressed
    dVamv = fin - fout
    
    # A13: Flow to thoracic veins
    Qamv = (Pamv - Ptv) / Rtv
    
    return dVamv, Qamv, Pamv


def musclePumpActivation(t, Tc, Tim):
    """
    Muscle pump activation function (Magosso & Ursino 2002 Equation 3)
    
    ψ(t) = {
        sin(π · Tim/Tc · α)     if 0 ≤ α ≤ Tc/Tim
        0                        if Tc/Tim ≤ α ≤ 1
    }
    
    where α = (t mod Tc) / Tc is the dimensionless cycle fraction
    
    Parameters:
    - t: current time
    - Tc: muscle contraction cycle duration (e.g., 1 s for running)
    - Tim: muscle contraction duration (e.g., 0.4 s)
    
    Returns:
    - psi: activation function (0-1)
    - alpha: dimensionless cycle fraction (0-1)
    """
    # Dimensionless cycle fraction
    alpha = (t % Tc) / Tc
    
    # Activation function
    if alpha <= (Tim / Tc):
        # Contraction phase - sinusoidal rise
        psi = np.sin(np.pi * (Tim / Tc) * alpha)
    else:
        # Relaxation phase
        psi = 0.0
    
    return psi, alpha


def intramuscularPressure(t, A_pump, Tc, Tim):
    """
    Intramuscular pressure during exercise (Magosso & Ursino 2002 Equation 2)
    
    Pim = A · ψ(t)
    
    where:
    - A is the peak value of intramuscular pressure (mmHg)
    - ψ(t) is the muscle activation function (0-1)
    
    Parameters:
    - t: current time
    - A_pump: peak intramuscular pressure amplitude (mmHg)
    - Tc: muscle contraction cycle duration (s)
    - Tim: muscle contraction duration (s)
    
    Returns:
    - Pim: intramuscular pressure (mmHg)
    - psi: activation function (0-1)
    - alpha: dimensionless cycle fraction (0-1)
    """
    psi, alpha = musclePumpActivation(t, Tc, Tim)
    Pim = A_pump * psi
    
    return Pim, psi, alpha
