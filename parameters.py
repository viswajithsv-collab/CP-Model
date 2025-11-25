"""
parameters.py

Parameter file for the Albanese 2016 Cardiopulmonary Model

Sources:
- Albanese et al. 2016: Table 1 (vascular system parameters)

Units:
- Compliance: mL/mmHg
- Unstressed volume: mL
- Resistance: mmHg·s/mL
- Inertance: mmHg·s²/mL

Author: Viswajith
Date: November 2024
"""

# =============================================================================
# SYSTEMIC CIRCULATION PARAMETERS (Albanese Table 1)
# =============================================================================

systemicParams = {
    # --- Systemic Arteries ---
    'Csa': 0.28,  # mL/mmHg
    'Vusa': 0.0,  # mL
    'Rsa': 0.06,  # mmHg·s/mL
    'Lsa': 0.22e-3,  # mmHg·s²/mL

    # --- Splanchnic Peripheral ---
    'Csp': 2.05,  # mL/mmHg
    'Vusp': 241.47,  # mL
    'Rsp': 3.307,  # mmHg·s/mL

    # --- Extrasplanchnic Peripheral ---
    'Cep': 0.668,  # mL/mmHg
    'Vuep': 118.48,  # mL
    'Rep': 3.52,  # mmHg·s/mL

    # --- Active Muscle Peripheral ---
    'Camp': 0.315,  # mL/mmHg
    'Vuamp': 55.86,  # mL
    'Ramp': 7.46,  # mmHg·s/mL

    # --- Resting Muscle Peripheral ---
    'Crmp': 0.21,  # mL/mmHg
    'Vurmp': 37.24,  # mL
    'Rrmp': 11.2,  # mmHg·s/mL

    # --- Brain Peripheral ---
    'Cbp': 0.358,  # mL/mmHg
    'Vubp': 63.47,  # mL
    'Rbp': 6.57,  # mmHg·s/mL

    # --- Coronary Peripheral ---
    'Chp': 0.119,  # mL/mmHg
    'Vuhp': 21.12,  # mL
    'Rhp': 19.71,  # mmHg·s/mL

    # --- Splanchnic Venous ---
    'Csv': 43.11,  # mL/mmHg
    'Vusv': 986.48,  # mL
    'Rsv': 0.038,  # mmHg·s/mL

    # --- Extrasplanchnic Venous ---
    'Cev': 14.0,  # mL/mmHg
    'Vuev': 484.0,  # mL
    'Rev': 0.04,  # mmHg·s/mL

    # --- Active Muscle Venous ---
    'Camv': 6.6,  # mL/mmHg
    'Vuamv': 228.17,  # mL
    'Ramv': 0.0833,  # mmHg·s/mL

    # --- Resting Muscle Venous ---
    'Crmv': 4.4,  # mL/mmHg
    'Vurmv': 152.11,  # mL
    'Rrmv': 0.125,  # mmHg·s/mL

    # --- Brain Venous ---
    'Cbv': 7.5,  # mL/mmHg
    'Vubv': 259.28,  # mL
    'Rbv': 0.075,  # mmHg·s/mL

    # --- Coronary Venous ---
    'Chv': 2.5,  # mL/mmHg
    'Vuhv': 86.42,  # mL
    'Rhv': 0.224,  # mmHg·s/mL

    # --- Thoracic Veins ---
    'Ctv': 33.0,  # mL/mmHg
    'Vutv': 0.0,  # mL
    'Rtv': 0.0054,  # mmHg·s/mL

    # --- Intramuscular Pressure (Eq 2-3) ---
    'A_pump': 50.0,  # mmHg (A = 50 mmHg)
    'Tim': 1.0,  # s
    'Tc': 0.75,  # s

    # --- Footnote Parameters ---
    'P0_amv': 3.93,  # mmHg (P0 in Eq 1)
    'kr_am': 24.17,  # s/mL (kr,am in Eq 12)
    'TBV': 5300.0,  # mL (total blood volume)
}

# =============================================================================
# PULMONARY CIRCULATION PARAMETERS (Albanese Table 1)
# =============================================================================

pulmonaryParams = {
    # --- Pulmonary Arteries ---
    'Cpa': 0.76,  # mL/mmHg
    'Vu_pa': 0.0,  # mL
    'Rpa': 0.023,  # mmHg·s/mL
    'Lpa': 0.18e-3,  # mmHg·s²/mL

    # --- Pulmonary Peripheral ---
    'Cpp': 5.8,  # mL/mmHg
    'Vu_pp': 108.2,  # mL
    'Rpp': 0.0894,  # mmHg·s/mL

    # --- Pulmonary Veins ---
    'Cpv': 25.37,  # mL/mmHg
    'Vu_pv': 105.6,  # mL
    'Rpv': 0.0056,  # mmHg·s/mL
}

# =============================================================================
# INTRATHORACIC AND ABDOMINAL PRESSURE (Albanese Table 1, Eq 4-10)
# =============================================================================

respiratoryPumpParams = {
    # --- Respiratory Timing ---
    'Tresp': 4.0,  # s (respiratory period)
    'Ti': 1.6,  # s (inspiration time)
    'Te': 1.4,  # s (expiration time)

    # --- Intrathoracic Pressure ---
    'Pthor_min_n': -9.0,  # mmHg
    'Pthor_max_n': -4.0,  # mmHg
    'gthor': 6.8,  # mmHg/L

    # --- Abdominal Pressure ---
    'Pabd_min_n': -2.5,  # mmHg
    'Pabd_max_n': 0.0,  # mmHg
    'gabd': 3.39,  # mmHg/L
}

# =============================================================================
# THORACIC VEINS PARAMETERS (Albanese Table 2, Eq 2-3)
# =============================================================================

thoracicVeinsParams = {
    # --- Pressure-Volume Relationship ---
    'D1': 0.3855,  # mmHg
    'K1': 0.15,  # mmHg/mL
    'Vutv': 130.0,  # mL (unstressed volume)
    'D2': -3.0,  # mmHg
    'K2': 0.4,  # mmHg
    'Vtv_min': 50.0,  # mL
    'Kxp': 2.0,  # mmHg
    'Kxv': 8.0,  # mL

    # --- Resistance ---
    'KR': 0.001,  # mmHg·s·mL^-1
    'Vtv_max': 350.0,  # mL
    'Rtv_0': 0.025,  # mmHg·s·mL^-1
}

# =============================================================================
# LUNG MECHANICS PARAMETERS (Albanese Table 3, Eq A30-A41)
# =============================================================================

lungMechanicsParams = {
    # --- Airway Compliances (L/cmH2O) ---
    'Cl': 0.00127,  # L/cmH2O - Larynx
    'Ct': 0.00238,  # L/cmH2O - Trachea
    'Cb': 0.0131,  # L/cmH2O - Bronchi
    'CA': 0.2,  # L/cmH2O - Alveolar

    # --- Unstressed Volumes (mL) ---
    'Vul': 34.4,  # mL - Larynx
    'Vut': 6.63,  # mL - Trachea
    'Vub': 18.7,  # mL - Bronchi
    'VuA': 1.263,  # L [MODEL] - Alveolar (1263 mL)

    # --- Airway Resistances (cmH2O·s·L^-1) ---
    'Rml': 1.021,  # cmH2O·s/L - Mouth to larynx
    'Rlt': 0.3369,  # cmH2O·s/L - Larynx to trachea
    'Rtb': 0.3063,  # cmH2O·s/L - Trachea to bronchi
    'RbA': 0.0817,  # cmH2O·s/L - Bronchi to alveoli

    # --- Additional Parameters ---
    'Ccw': 0.2445,  # L/cmH2O - Chest wall compliance
    'RR': 12.0,  # breaths/min - Respiratory rate [MODEL]
    'IEratio': 0.6,  # I:E ratio [MODEL]
    'FRC': 2.4,  # L - Functional residual capacity
    'Ppl_ref': -5.0,  # cmH2O - Reference pleural pressure
    'Pmus_min': -5.0,  # cmH2O - Peak inspiratory muscle pressure [MODEL]
    'tau': 0.2,  # s - Time constant (Tr/5) [MODEL]
}

# =============================================================================
# TISSUE GAS EXCHANGE PARAMETERS (Albanese Table 5, Eq A57-A78)
# =============================================================================

tissueGasExchangeParams = {
    # --- Tissue Volumes (mL) ---
    'VT_hp': 284.0,  # mL - Coronary tissue volume
    'VT_bp': 1300.0,  # mL - Brain tissue volume
    'VT_mp': 31200.0,  # mL - Skeletal muscle tissue volume
    'VT_sp': 2673.0,  # mL - Splanchnic tissue volume
    'VT_ep': 262.0,  # mL - Extrasplanchnic tissue volume

    # --- O2 Consumption Rates (mL/min) ---
    'MO2_hp': 24.0,  # mL/min - Coronary O2 consumption
    'MO2_bp': 47.502,  # mL/min - Brain O2 consumption
    'MO2_mp': 51.6,  # mL/min - Skeletal muscle O2 consumption
    'MO2_sp': 108.419,  # mL/min - Splanchnic O2 consumption
    'MO2_ep': 14.683,  # mL/min - Extrasplanchnic O2 consumption

    # --- CO2 Production Rates (mL/min) [MODEL] ---
    'MCO2_hp': 20.16,  # mL/min - Coronary CO2 production
    'MCO2_bp': 39.961,  # mL/min - Brain CO2 production
    'MCO2_mp': 43.344,  # mL/min - Skeletal muscle CO2 production
    'MCO2_sp': 91.072,  # mL/min - Splanchnic CO2 production
    'MCO2_ep': 12.337,  # mL/min - Extrasplanchnic CO2 production

    # --- Blood Transport Delays (s) [MODEL] ---
    'tau_LT': 18.0,  # s - Lung to tissue delay
    'tau_TL': 10.0,  # s - Tissue to lung delay
}

# =============================================================================
# LUNG GAS EXCHANGE PARAMETERS (Albanese Table 4, Eq A42-A56)
# =============================================================================

lungGasExchangeParams = {
    # --- Environmental Conditions ---
    'FiO2': 0.21037,  # Inspired O2 fraction
    'FiCO2': 0.00421,  # Inspired CO2 fraction
    'K': 1.2103,  # Gas constant factor
    'Patm': 760.0,  # mmHg - Atmospheric pressure
    'Pws': 47.0,  # mmHg - Water vapor pressure at 37°C

    # --- O2 Dissociation Curve (Eq 60) ---
    'Csat_O2': 9.0,  # mmol/L - O2 saturation concentration
    'h1': 0.3836,  # O2 dissociation parameter
    'alpha1': 0.03198,  # mmHg^-1 - O2 dissociation parameter
    'beta1': 0.008275,  # mmHg^-1 - O2 dissociation parameter
    'K1_O2': 14.99,  # mmHg - O2 dissociation parameter

    # --- CO2 Dissociation Curve ---
    'Csat_CO2': 86.11,  # mmol/L - CO2 saturation concentration
    'h2': 1.819,  # CO2 dissociation parameter
    'alpha2': 0.05591,  # mmHg^-1 - CO2 dissociation parameter
    'beta2': 0.03255,  # mmHg^-1 - CO2 dissociation parameter
    'K2_CO2': 194.4,  # mmHg - CO2 dissociation parameter

    # --- Physiological Status ---
    'sh': 1.7,  # Shunt fraction parameter (Eq 33)
    'Hgb': 15.0,  # g/dL - Hemoglobin concentration (Eq 72)
}

# =============================================================================
# RESPIRATORY CONTROL PARAMETERS (Albanese Table 6, Eq A79-A84)
# =============================================================================

respiratoryControlParams = {
    # --- Peripheral Chemoreceptors ---
    'Dp': 7.0,  # s - Peripheral delay
    'tau_pA': 83.0,  # s - Peripheral time constant [MODEL]
    'Gp_A': 1.310,  # cmH2O/v - Peripheral gain [MODEL]
    'tau_p_f': 147.78,  # s - Peripheral freq time constant [MODEL]
    'Gp_f': 0.8735,  # breaths·min^-1·v^-1 - Peripheral freq gain [MODEL]
    'f_pn': 3.7,  # spikes/s - Peripheral baseline firing

    # --- Central Chemoreceptors ---
    'Dc': 8.0,  # s - Central delay
    'tau_cA': 105.0,  # s - Central time constant [MODEL]
    'Gc_A': 850.0,  # cmH2O/mmHg - Central gain [MODEL]
    'tau_c_f': 400.0,  # s - Central freq time constant [MODEL]
    'Gc_f': 0.9,  # breaths·min^-1·mmHg^-1 - Central freq gain [MODEL]
    'PaCO2_n': 40.0,  # mmHg - Normal arterial PCO2
}

# =============================================================================
# CARDIOVASCULAR CONTROL PARAMETERS (Albanese Table 7, modified from Ursino/Magosso)
# =============================================================================

cardiovascularControlParams = {
    # --- Afferent Lung Stretch Receptors ---
    'G_lsr': 11.76,  # spikes·L^-1·s^-1 - Lung stretch receptor gain

    # --- Efferent Sympathetic Pathway ---
    'Wb_sp': -1.1375,  # Sympathetic weight - splanchnic
    'Wb_sv': -1.0806,  # Sympathetic weight - splanchnic venous
    'Wb_sh': -1.75,  # Sympathetic weight - heart
    'Wp_sp': 1.716,  # Parasympathetic weight - splanchnic
    'Wp_sv': 1.716,  # Parasympathetic weight - splanchnic venous
    'Ws_sp': -0.3997,  # Weight parameter - splanchnic
    'Ws_sv': -0.2907,  # Weight parameter - splanchnic venous

    # --- Autoregulation ---
    'g_bO2': 140.0,  # mL blood/mL O2 - Brain O2 autoregulation
    'g_mO2': 490.0,  # blood/mL O2 - Muscle O2 autoregulation
    'g_hO2': 420.0,  # blood/mL O2 - Coronary O2 autoregulation
}

# =============================================================================
# BARORECEPTOR PARAMETERS (Ursino 1998 Table 3, Eq 30-31)
# =============================================================================

baroreceptorParams = {
    # --- Carotid Sinus Afferent Pathway ---
    'Pn': 92.0,  # mmHg - Setpoint pressure
    'ka': 11.758,  # mmHg - Slope parameter
    'tau_z': 6.37,  # s - Zero time constant
    'tau_p': 2.076,  # s - Pole time constant
    'f_min': 2.52,  # spikes/s - Minimum firing rate
    'f_max': 47.78,  # spikes/s - Maximum firing rate

    # --- Sympathetic Efferent Pathway (Eq 33) ---
    'f_es_inf': 2.10,  # spikes/s - Lower asymptote
    'f_es_0': 16.11,  # spikes/s - Upper asymptote
    'f_es_min': 2.66,  # spikes/s - Minimum sympathetic
    'k_es': 0.0675,  # s - Slope parameter

    # --- Vagal Efferent Pathway (Eq 34) ---
    'f_ev_0': 3.2,  # spikes/s - Lower asymptote
    'f_ev_inf': 6.3,  # spikes/s - Upper asymptote
    'f_ab_0': 25.0,  # spikes/s - Baseline afferent firing
    'k_ev': 7.06,  # spikes/s - Slope parameter
}

# =============================================================================
# SYMPATHETIC EFFECTOR PARAMETERS (Ursino 1998 Table 3, Eq 35-42)
# =============================================================================

sympatheticEffectorParams = {
    # --- Resistance Control Gains ---
    'G_Rsp': 0.475,  # mmHg·mL^-1·v^-1 - Splanchnic resistance gain
    'G_Rep': 0.282,  # mmHg·mL^-1·v^-1 - Extrasplanchnic resistance gain
    'G_Rmp': 0.695,  # mmHg·s·mL^-1·v^-1 - Muscle resistance gain
    'G_Rhp': 0.53,  # mmHg·s·mL^-1·v^-1 - Coronary resistance gain

    # --- Unstressed Volume Control Gains ---
    'G_Vusp': -265.4,  # mL/v - Splanchnic unstressed volume gain
    'G_Vuev': -132.5,  # mL/v - Extrasplanchnic venous unstressed volume gain
    'G_Vumv': -0.13,  # s/v - Muscle venous unstressed volume gain
    'G_Ts': 0.09,  # s/v - Heart period sympathetic gain

    # --- Resistance Time Constants ---
    'tau_Rsp': 8.0,  # s - Splanchnic resistance time constant
    'tau_Rep': 8.0,  # s - Extrasplanchnic resistance time constant
    'tau_Rmp': 6.0,  # s - Muscle resistance time constant
    'tau_Rhp': 6.0,  # s - Coronary resistance time constant

    # --- Unstressed Volume Time Constants ---
    'tau_Vusp': 20.0,  # s - Splanchnic Vu time constant
    'tau_Vuev': 20.0,  # s - Extrasplanchnic Vu time constant
    'tau_Vumv': 20.0,  # s - Muscle Vu time constant
    'tau_Ts': 2.0,  # s - Heart period sympathetic time constant
    'tau_Tv': 1.5,  # s - Heart period vagal time constant

    # --- Resistance Delays ---
    'D_Rsp': 2.0,  # s - Splanchnic resistance delay
    'D_Rep': 2.0,  # s - Extrasplanchnic resistance delay
    'D_Rmp': 2.0,  # s - Muscle resistance delay
    'D_Rhp': 2.0,  # s - Coronary resistance delay

    # --- Unstressed Volume Delays ---
    'D_Vusp': 5.0,  # s - Splanchnic Vu delay
    'D_Vuev': 5.0,  # s - Extrasplanchnic Vu delay
    'D_Vumv': 5.0,  # s - Muscle Vu delay
    'D_Ts': 2.0,  # s - Heart period sympathetic delay
    'D_Tv': 0.2,  # s - Heart period vagal delay

    # --- Elastance Control ---
    'Emax_lv_0': 2.392,  # mmHg/mL - Baseline LV max elastance
    'Emax_rv_0': 1.412,  # mmHg/mL - Baseline RV max elastance
    'R_sp_0': 2.49,  # mmHg·s·mL^-1 - Baseline splanchnic resistance
    'R_ep_0': 0.78,  # mmHg·s·mL^-1 - Baseline extrasplanchnic resistance
    'Vu_sv_0': 1435.4,  # mL - Baseline splanchnic venous Vu
    'Vu_ev_0': 1537.0,  # mL - Baseline extrasplanchnic venous Vu
    'T_0': 0.58,  # s - Intrinsic heart period
}

# =============================================================================
# MAGOSSO 2002 EXERCISE PARAMETERS (Table 2)
# =============================================================================

magossoExerciseParams = {
    # --- Efferent Sympathetic and Vagal Pathways (Eq 13-14) ---
    'f_es_inf_m': 2.10,  # s^-1 - Sympathetic lower asymptote
    'f_es_0_m': 16.11,  # s^-1 - Sympathetic upper asymptote
    'f_es_max': 60.0,  # s^-1 - Maximum sympathetic firing
    'k_es_m': 0.0675,  # s - Sympathetic slope
    'Wb_sp_m': -1.0,  # Weight - splanchnic baroreflex
    'Wb_sv_m': -1.0,  # Weight - splanchnic venous baroreflex
    'Wb_sh_m': -1.0,  # Weight - heart baroreflex
    'Wp_sp_m': -0.34,  # Weight - splanchnic peripheral
    'Wp_sv_m': -0.34,  # Weight - splanchnic venous peripheral
    'Wp_sh_m': 0.0,  # Weight - heart peripheral
    'theta_sp': -4.6,  # spikes/s - Splanchnic threshold
    'theta_sv': -4.6,  # spikes/s - Splanchnic venous threshold
    'theta_sh': 0.0,  # spikes/s - Heart threshold
    'f_ev_0_m': 3.2,  # spikes/s - Vagal lower asymptote
    'f_ev_inf_m': 6.3,  # spikes/s - Vagal upper asymptote
    'f_ab_0_m': 25.15,  # spikes/s - Baseline afferent firing
    'Wp_v': -0.103,  # Vagal peripheral weight
    'theta_v': -1.4,  # spikes/s - Vagal threshold
    'k_ev_m': 7.06,  # spikes/s - Vagal slope

    # --- Central Command (Eq 15) ---
    'gamma_sp_min': -0.037,  # spikes/s - Splanchnic min
    'gamma_sv_min': -0.437,  # spikes/s - Splanchnic venous min
    'gamma_sh_min': -0.0283,  # spikes/s - Heart min
    'gamma_v_min': -0.0008,  # spikes/s - Vagal min
    'gamma_sp_max': 5.5,  # spikes/s - Splanchnic max
    'gamma_sv_max': 64.9,  # spikes/s - Splanchnic venous max
    'gamma_sh_max': 9.0,  # spikes/s - Heart max
    'gamma_v_max': 1.9,  # spikes/s - Vagal max
    'I0_sp': 0.65,  # Central command threshold - splanchnic
    'I0_sv': 0.45,  # Central command threshold - splanchnic venous
    'I0_sh': 0.658,  # Central command threshold - heart
    'I0_v': 0.126,  # Central command threshold - vagal
    'k_cc_sp': 0.13,  # Central command slope - splanchnic
    'k_cc_sv': 0.09,  # Central command slope - splanchnic venous
    'k_cc_sh': 0.114,  # Central command slope - heart
    'k_cc_v': 0.0162,  # Central command slope - vagal

    # --- Metabolic Regulation (Eq 16-26) ---
    'g_am_O2': 30.0,  # Active muscle O2 gain
    'M_am_n': 0.516,  # mL/s - Baseline active muscle metabolism
    'phi_min': -1.87,  # Minimum metabolic factor
    'tau_met': 10.0,  # s - Metabolic time constant
    'g_h_O2': 35.0,  # Coronary O2 gain
    'Wh_n': 12660.0,  # mmHg·mL·s^-1 - Baseline cardiac work
    'Cvam_O2_n': 0.1555,  # mL/mL - Active muscle venous O2
    'g_M': 40.0,  # Metabolic gain factor
    'phi_max': 20.0,  # Maximum metabolic factor
    'D_met': 4.0,  # s - Metabolic delay
    'Cvh_O2_n': 0.11,  # mL/mL - Coronary venous O2
    'tau_w': 5.0,  # s - Cardiac work time constant
    'Ca_O2': 0.2,  # mL/mL - Arterial O2 concentration
    'tau_M': 40.0,  # s - Metabolic time constant (long)
    'I0_met': 0.4266,  # Metabolic intensity threshold
    'k_met': 0.18,  # Metabolic slope
    'tau_O2': 10.0,  # s - O2 time constant
    'Mh_n': 0.4,  # mL/s - Baseline cardiac O2 consumption

    # --- Respiratory Response (Eq 27-33) ---
    'Vdot_n': 8.7,  # L/min - Baseline minute ventilation
    'VT_n': 0.583,  # L - Baseline tidal volume
    'A_vent': 33.0,  # L/min - Ventilation gain A
    'B_vent': 61.0,  # L/min - Ventilation gain B
    'g_VT': 1.62,  # L - Tidal volume gain
    'D_V': 2.5,  # s - Ventilation delay
    'tau_V': 60.0,  # s - Ventilation time constant
}

# =============================================================================
# HEART MODEL PARAMETERS (Albanese Table A-3)
# =============================================================================

heartParams = {
    # --- Left Atrium ---
    'CLA': 19.23,  # mL/mmHg - Left atrial compliance
    'VLA_u': 16.7,  # mL - Left atrial unstressed volume
    'RLA': 2.5e-3,  # mmHg·s·mL^-1 - Left atrial resistance

    # --- Left Ventricle EDPVR (End-Diastolic Pressure-Volume) ---
    'PLV_0': 1.5,  # mmHg - Scaling factor for LV EDPVR
    'KLV_E': 0.017,  # mL^-1 - Exponent for LV EDPVR
    'VLV_u': 16.7,  # mL - LV unstressed volume

    # --- Left Ventricle ESPVR (End-Systolic Pressure-Volume) ---
    'ELV_plus': 2.9,  # mmHg/mL - Ascending slope for LV ESPVR
    'ELV_minus': None,  # mmHg/mL - Descending slope (not specified as --)
    'VLV_0': None,  # mL - Descending LV ESPVR pressure axis intercept (not specified)
    'KLV_R': 3.75e-4,  # s/mL - Scaling factor for LV viscous resistance

    # --- Right Atrium ---
    'CRA': 31.25,  # mL/mmHg - Right atrial compliance
    'VRA_u': 25.0,  # mL - Right atrial unstressed volume
    'RRA': 2.5e-3,  # mmHg·s·mL^-1 - Right atrial resistance

    # --- Right Ventricle EDPVR ---
    'PRV_0': 1.5,  # mmHg - Scaling factor for RV EDPVR
    'KRV_E': 0.016,  # mL^-1 - Exponent for RV EDPVR
    'VRV_u': 40.8,  # mL - RV unstressed volume

    # --- Right Ventricle ESPVR ---
    'ERV_plus': 1.75,  # mmHg/mL - Ascending slope for RV ESPVR
    'ERV_minus': None,  # mmHg/mL - Descending slope (not specified as --)
    'VRV_0': None,  # mL - Descending RV ESPVR pressure axis intercept (not specified)
    'KRV_R': 1.4e-3,  # s/mL - Scaling factor for RV viscous resistance

    # --- Interventricular Septum (Albanese Table A-4) ---
    'E_spt_es': 48.75,  # mmHg/mL - Septum end-systolic elastance
    'V_spt_d': 2.0,  # mL - Septum volume axis intercept
    'P_spt_0': 1.11,  # mmHg - Septal pressure intercept for end diastole
    'lambda_spt': 0.435,  # 1/mL - Empirical constant for P-V relationship
    'V_spt_0': 2.0,  # mL - Septal volume intercept for end diastole
}

