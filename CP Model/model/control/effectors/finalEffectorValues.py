"""
finalEffectorValues.py

Combines all effects (neural + local + exercise) to get the final values
that the cardiovascular system actually uses.
"""


def finalPeripheralResistance(dR, R_0, x_j_O2=0, x_j_CO2=0, exercise_metabolic=0):
    """
    Complete resistance: neural + local + exercise effects

    R_jpn = dR + R_0  (neural)
    R_jp = R_jpn * (1 + x_j_CO2 + exercise_metabolic) / (1 + x_j_O2)  (final)
    """
    R_jpn = dR + R_0
    R_jp = R_jpn * (1 + x_j_CO2 + exercise_metabolic) / (1 + x_j_O2)
    return max(R_jp, 0.01 * R_0)  # Prevent negative resistance


def finalVenousVolume(dV, V_u_0, muscle_pump_effect=0):
    """Complete venous volume: neural + exercise pump"""
    V_u = dV + V_u_0 + muscle_pump_effect
    return max(V_u, 0.1 * V_u_0)  # Prevent negative volume


def finalCardiacContractility(dE, E_max_0, exercise_contractility=0):
    """Complete contractility: neural + exercise effects"""
    E_max = dE + E_max_0 + exercise_contractility
    return max(E_max, 0.1 * E_max_0)  # Prevent negative contractility


def finalHeartPeriod(dT_s, dT_v, T_0, central_command=0, exercise_tachycardia=0):
    """Complete heart period: neural + exercise effects"""
    T = dT_s + dT_v + T_0 + central_command + exercise_tachycardia
    return max(min(T, 2.0), 0.24)  # Physiological limits: 30-250 bpm