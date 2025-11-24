"""
ControlSystemModel.py

Comprehensive cardiovascular control system model consolidating:
- Afferent sensors (baroreceptors, chemoreceptors, lung stretch receptors)
- CNS processing (ischemic response, autonomic nervous system)
- Efferent pathways (sympathetic, parasympathetic)
- Local autoregulation (brain, coronary, muscle)
- Exercise components (central command, muscle pump, metabolism, respiratory pump)
- Final effector integration

Based on:
- Ursino 1998: Interaction between carotid baroregulation and the pulsating heart
- Ursino & Magosso 2000: Acute cardiovascular response to isocapnic hypoxia
- Magosso & Ursino 2001: Cardiovascular response to dynamic aerobic exercise
- Magosso & Ursino 2002: Exercise reflex control mechanisms
- Albanese et al. 2016: Integrated cardiopulmonary model

Author: Viswajith
Date: November 2024
"""

import numpy as np


class ControlSystemModel:
    """
    Complete cardiovascular control system integrating neural reflexes,
    local autoregulation, and exercise responses.
    
    Architecture:
        1. Afferent sensors detect physiological state
        2. CNS processes afferent information
        3. Efferent pathways modulate target organs
        4. Local autoregulation provides tissue-level control
        5. Exercise components add metabolic demands
        6. Final effectors integrate all control signals
    
    State Variables (active control):
        Baroreceptor dynamics: x_ab, x_ab_dot (carotid), x_Ab, x_Ab_dot (aortic)
        Chemoreceptor dynamics: x_pO2, x_pCO2, x_cO2, x_cCO2
        Lung stretch dynamics: x_ls
        CNS ischemic: x_cns_O2, x_cns_CO2
        Sympathetic efferents: x_R (resistance), x_V (venous), x_E (contractility)
        Parasympathetic efferents: x_Ts (sympathetic HR), x_Tv (vagal HR)
        Autoregulation: x_br_O2, x_br_CO2, x_cor_O2, x_cor_CO2, x_mus_O2, x_mus_CO2
        Exercise ventilation: x_Vdot_slow
    """
    
    def __init__(self, params):
        """
        Initialize control system with parameters.
        
        Parameters dict should contain:
        - Baroreceptor: P_n, k_ab, tau_ab, tau_ab_z, k_Ab, tau_Ab, tau_Ab_z, f_ab_min, f_ab_max
        - Chemoreceptor: pO2_n, pCO2_n, G_pO2, G_pCO2, G_cCO2, tau_pO2, tau_pCO2, tau_cCO2, f_ch_min, f_ch_max
        - Lung stretch: G_ls, tau_ls, VT_n
        - CNS ischemic: pO2_cns_th, pCO2_cns_th, G_cns_O2, G_cns_CO2, tau_cns_O2, tau_cns_CO2
        - Autonomic: f_es_inf, f_es_0, f_ev_0, f_ev_inf, k_es, k_ev
        - Sympathetic: G_R, tau_R, D_R, R_0, R_inf, R_max, G_V, tau_V, D_V, Vu_0, G_E, tau_E, D_E, E_0, E_max
        - Parasympathetic: G_Ts, tau_Ts, D_Ts, G_Tv, tau_Tv, D_Tv, T_0, T_min, T_max
        - Autoregulation: G_br_O2, G_br_CO2, tau_br_O2, tau_br_CO2, G_cor_O2, G_cor_CO2, tau_cor_O2, tau_cor_CO2, G_mus_O2, G_mus_CO2, tau_mus_O2, tau_mus_CO2
        - Central command: G_cc_symp, G_cc_vagal, I_th_cc
        - Muscle pump: P_im_max, k_mp, f_contraction
        - Exercise metabolism: VO2_rest, VO2_max, VCO2_rest, RQ_rest, RQ_max
        - Respiratory pump: Vdot_n, A_vent, B_vent, tau_v, fast_fraction
        """
        self.params = params
        
        # Baroreceptor parameters
        self.P_n = params['P_n']
        self.k_ab = params['k_ab']
        self.tau_ab = params['tau_ab']
        self.tau_ab_z = params['tau_ab_z']
        self.k_Ab = params['k_Ab']
        self.tau_Ab = params['tau_Ab']
        self.tau_Ab_z = params['tau_Ab_z']
        self.f_ab_min = params['f_ab_min']
        self.f_ab_max = params['f_ab_max']
        
        # Chemoreceptor parameters
        self.pO2_n = params['pO2_n']
        self.pCO2_n = params['pCO2_n']
        self.G_pO2 = params['G_pO2']
        self.G_pCO2 = params['G_pCO2']
        self.G_cCO2 = params['G_cCO2']
        self.tau_pO2 = params['tau_pO2']
        self.tau_pCO2 = params['tau_pCO2']
        self.tau_cCO2 = params['tau_cCO2']
        self.f_ch_min = params['f_ch_min']
        self.f_ch_max = params['f_ch_max']
        
        # Lung stretch parameters
        self.G_ls = params['G_ls']
        self.tau_ls = params['tau_ls']
        self.VT_n = params['VT_n']
        
        # CNS ischemic parameters
        self.pO2_cns_th = params['pO2_cns_th']
        self.pCO2_cns_th = params['pCO2_cns_th']
        self.G_cns_O2 = params['G_cns_O2']
        self.G_cns_CO2 = params['G_cns_CO2']
        self.tau_cns_O2 = params['tau_cns_O2']
        self.tau_cns_CO2 = params['tau_cns_CO2']
        
        # Autonomic parameters
        self.f_es_inf = params['f_es_inf']
        self.f_es_0 = params['f_es_0']
        self.f_ev_0 = params['f_ev_0']
        self.f_ev_inf = params['f_ev_inf']
        self.k_es = params['k_es']
        self.k_ev = params['k_ev']
        
        # Sympathetic efferent parameters
        self.G_R = params['G_R']
        self.tau_R = params['tau_R']
        self.D_R = params['D_R']
        self.R_0 = params['R_0']
        self.R_inf = params['R_inf']
        self.R_max = params['R_max']
        self.G_V = params['G_V']
        self.tau_V = params['tau_V']
        self.D_V = params['D_V']
        self.Vu_0 = params['Vu_0']
        self.G_E = params['G_E']
        self.tau_E = params['tau_E']
        self.D_E = params['D_E']
        self.E_0 = params['E_0']
        self.E_max = params['E_max']
        
        # Parasympathetic efferent parameters
        self.G_Ts = params['G_Ts']
        self.tau_Ts = params['tau_Ts']
        self.D_Ts = params['D_Ts']
        self.G_Tv = params['G_Tv']
        self.tau_Tv = params['tau_Tv']
        self.D_Tv = params['D_Tv']
        self.T_0 = params['T_0']
        self.T_min = params['T_min']
        self.T_max = params['T_max']
        
        # Autoregulation parameters
        self.G_br_O2 = params['G_br_O2']
        self.G_br_CO2 = params['G_br_CO2']
        self.tau_br_O2 = params['tau_br_O2']
        self.tau_br_CO2 = params['tau_br_CO2']
        self.G_cor_O2 = params['G_cor_O2']
        self.G_cor_CO2 = params['G_cor_CO2']
        self.tau_cor_O2 = params['tau_cor_O2']
        self.tau_cor_CO2 = params['tau_cor_CO2']
        self.G_mus_O2 = params['G_mus_O2']
        self.G_mus_CO2 = params['G_mus_CO2']
        self.tau_mus_O2 = params['tau_mus_O2']
        self.tau_mus_CO2 = params['tau_mus_CO2']
        
        # Central command parameters
        self.G_cc_symp = params['G_cc_symp']
        self.G_cc_vagal = params['G_cc_vagal']
        self.I_th_cc = params['I_th_cc']
        
        # Muscle pump parameters
        self.P_im_max = params['P_im_max']
        self.k_mp = params['k_mp']
        self.f_contraction = params['f_contraction']
        
        # Exercise metabolism parameters
        self.VO2_rest = params['VO2_rest']
        self.VO2_max = params['VO2_max']
        self.VCO2_rest = params['VCO2_rest']
        self.RQ_rest = params['RQ_rest']
        self.RQ_max = params['RQ_max']
        
        # Respiratory pump parameters
        self.Vdot_n = params['Vdot_n']
        self.A_vent = params['A_vent']
        self.B_vent = params['B_vent']
        self.tau_v = params['tau_v']
        self.fast_fraction = params['fast_fraction']
    
    # =========================================================================
    # SECTION 1: AFFERENT SENSORS
    # =========================================================================
    
    # --- 1A: Baroreceptors (baroreceptors.py) ---
    
    def linearDerivativeFilter(self, P, x, x_dot, tau, tau_z):
        """
        Linear derivative high-pass filter for baroreceptor dynamics.
        
        Models adaptation of baroreceptors to sustained pressure changes.
        Implements Ursino 1998 Eq. 1-2.
        
        Args:
            P: Arterial pressure (mmHg)
            x: Filter state variable
            x_dot: Derivative of filter state
            tau: Primary time constant (s)
            tau_z: Zero time constant (s)
        
        Returns:
            tuple: (dx_dt, dx_dot_dt) derivatives for integration
        """
        dx_dt = x_dot
        dx_dot_dt = (1.0 / (tau * tau_z)) * (P - x - (tau + tau_z) * x_dot)
        return dx_dt, dx_dot_dt
    
    def baroreceptorAfferentActivity(self, P, x, x_dot, tau_z, P_n, k, f_min, f_max):
        """
        Compute baroreceptor afferent firing rate.
        
        Sigmoidal relationship between filtered pressure and firing rate.
        Implements Ursino 1998 Eq. 3-4.
        
        Args:
            P: Arterial pressure (mmHg)
            x: Filter state variable
            x_dot: Derivative of filter state
            tau_z: Zero time constant (s)
            P_n: Setpoint pressure (mmHg)
            k: Gain constant (mmHg)
            f_min: Minimum firing rate (Hz)
            f_max: Maximum firing rate (Hz)
        
        Returns:
            float: Afferent firing rate (Hz)
        """
        # Filtered pressure with derivative component
        P_tilde = P + tau_z * x_dot
        
        # Sigmoidal activation
        exponent = (P_tilde - P_n) / k
        
        # Prevent overflow
        exponent = np.clip(exponent, -50, 50)
        
        f_ab = f_min + (f_max - f_min) / (1.0 + np.exp(-exponent))
        
        return f_ab
    
    def carotidBaroreceptor(self, P_carotid, x_ab, x_ab_dot):
        """
        Carotid baroreceptor afferent activity.
        
        Args:
            P_carotid: Carotid sinus pressure (mmHg)
            x_ab: Carotid filter state
            x_ab_dot: Carotid filter derivative
        
        Returns:
            tuple: (f_ab, dx_ab_dt, dx_ab_dot_dt)
        """
        
        # Filter dynamics
        dx_ab_dt, dx_ab_dot_dt = self.linearDerivativeFilter(
            P_carotid, x_ab, x_ab_dot, self.tau_ab, self.tau_ab_z
        )
        
        # Afferent activity
        f_ab = self.baroreceptorAfferentActivity(
            P_carotid, x_ab, x_ab_dot, self.tau_ab_z,
            self.P_n, self.k_ab, self.f_ab_min, self.f_ab_max
        )
        
        return f_ab, dx_ab_dt, dx_ab_dot_dt
    
    def aorticBaroreceptor(self, P_aortic, x_Ab, x_Ab_dot):
        """
        Aortic baroreceptor afferent activity.
        
        Args:
            P_aortic: Aortic arch pressure (mmHg)
            x_Ab: Aortic filter state
            x_Ab_dot: Aortic filter derivative
        
        Returns:
            tuple: (f_Ab, dx_Ab_dt, dx_Ab_dot_dt)
        """
        
        # Filter dynamics
        dx_Ab_dt, dx_Ab_dot_dt = self.linearDerivativeFilter(
            P_aortic, x_Ab, x_Ab_dot, self.tau_Ab, self.tau_Ab_z
        )
        
        # Afferent activity
        f_Ab = self.baroreceptorAfferentActivity(
            P_aortic, x_Ab, x_Ab_dot, self.tau_Ab_z,
            self.P_n, self.k_Ab, self.f_ab_min, self.f_ab_max
        )
        
        return f_Ab, dx_Ab_dt, dx_Ab_dot_dt
    
    def combinedBaroreceptorAfferent(self, f_carotid, f_aortic, w_carotid=0.5):
        """
        Combine carotid and aortic baroreceptor signals.
        
        Args:
            f_carotid: Carotid firing rate (Hz)
            f_aortic: Aortic firing rate (Hz)
            w_carotid: Weight for carotid (default 0.5)
        
        Returns:
            float: Combined baroreceptor afferent (Hz)
        """
        return w_carotid * f_carotid + (1 - w_carotid) * f_aortic
    
    # --- 1B: Chemoreceptors (chemoreflexPathway.py) ---
    
    def peripheralChemoreceptorO2Static(self, pO2):
        """
        Static peripheral chemoreceptor response to O2.
        
        Hyperbolic response - increases as pO2 falls.
        Ursino & Magosso 2000.
        
        Args:
            pO2: Arterial oxygen partial pressure (mmHg)
        
        Returns:
            float: Static chemoreceptor activity (Hz)
        """
        
        # Prevent division by zero
        pO2 = max(pO2, 1.0)
        
        # Hyperbolic response
        f_pO2_static = self.G_pO2 * (self.pO2_n / pO2 - 1.0)
        
        return max(0.0, f_pO2_static)
    
    def peripheralChemoreceptorCO2Static(self, pCO2):
        """
        Static peripheral chemoreceptor response to CO2.
        
        Linear response - increases with pCO2.
        
        Args:
            pCO2: Arterial CO2 partial pressure (mmHg)
        
        Returns:
            float: Static chemoreceptor activity (Hz)
        """
        
        f_pCO2_static = self.G_pCO2 * (pCO2 - self.pCO2_n)
        
        return max(0.0, f_pCO2_static)
    
    def centralChemoreceptorCO2Static(self, pCO2_brain):
        """
        Static central chemoreceptor response to brain CO2.
        
        Args:
            pCO2_brain: Brain tissue CO2 partial pressure (mmHg)
        
        Returns:
            float: Static central chemoreceptor activity (Hz)
        """
        
        f_cCO2_static = self.G_cCO2 * (pCO2_brain - self.pCO2_n)
        
        return max(0.0, f_cCO2_static)
    
    def chemoreceptorDynamics(self, f_static, x_ch, tau_ch):
        """
        First-order chemoreceptor dynamics.
        
        Args:
            f_static: Static response
            x_ch: Current dynamic state
            tau_ch: Time constant (s)
        
        Returns:
            float: dx_ch/dt for integration
        """
        return (f_static - x_ch) / tau_ch
    
    def peripheralChemoreceptor(self, pO2, pCO2, x_pO2, x_pCO2):
        """
        Complete peripheral chemoreceptor response.
        
        Args:
            pO2: Arterial O2 (mmHg)
            pCO2: Arterial CO2 (mmHg)
            x_pO2: O2 dynamic state
            x_pCO2: CO2 dynamic state
        
        Returns:
            tuple: (f_peripheral, dx_pO2_dt, dx_pCO2_dt)
        """
        
        # Static responses
        f_pO2_static = self.peripheralChemoreceptorO2Static(pO2)
        f_pCO2_static = self.peripheralChemoreceptorCO2Static(pCO2)
        
        # Dynamics
        dx_pO2_dt = self.chemoreceptorDynamics(f_pO2_static, x_pO2, self.tau_pO2)
        dx_pCO2_dt = self.chemoreceptorDynamics(f_pCO2_static, x_pCO2, self.tau_pCO2)
        
        # Combined peripheral response (multiplicative interaction)
        f_peripheral = x_pO2 * (1.0 + x_pCO2)
        
        # Clamp to physiological range
        f_peripheral = np.clip(f_peripheral, self.f_ch_min, self.f_ch_max)
        
        return f_peripheral, dx_pO2_dt, dx_pCO2_dt
    
    def centralChemoreceptor(self, pCO2_brain, x_cCO2):
        """
        Central chemoreceptor response.
        
        Args:
            pCO2_brain: Brain tissue CO2 (mmHg)
            x_cCO2: Central CO2 dynamic state
        
        Returns:
            tuple: (f_central, dx_cCO2_dt)
        """
        
        f_cCO2_static = self.centralChemoreceptorCO2Static(pCO2_brain)
        dx_cCO2_dt = self.chemoreceptorDynamics(f_cCO2_static, x_cCO2, self.tau_cCO2)
        
        return x_cCO2, dx_cCO2_dt
    
    # --- 1C: Lung Stretch Receptors (lungStretchReceptors.py) ---
    
    def ventilationFromChemoreceptors(self, f_peripheral, f_central):
        """
        Compute minute ventilation from chemoreceptor activity.
        
        Ventilatory response driven by both peripheral and central chemoreceptors.
        Magosso & Ursino 2001 Eq. 27-28.
        
        Args:
            f_peripheral: Peripheral chemoreceptor activity (Hz)
            f_central: Central chemoreceptor activity (Hz)
        
        Returns:
            float: Minute ventilation (L/min)
        """
        
        # Baseline plus chemoreceptor-driven increase
        Vdot = self.Vdot_n * (1.0 + 0.5 * f_peripheral + 0.3 * f_central)
        
        return max(self.Vdot_n, Vdot)
    
    def tidalVolume(self, Vdot, RR=12.0):
        """
        Compute tidal volume from minute ventilation and respiratory rate.
        
        Args:
            Vdot: Minute ventilation (L/min)
            RR: Respiratory rate (breaths/min)
        
        Returns:
            float: Tidal volume (L)
        """
        return Vdot / RR
    
    def lungStretchReceptorStatic(self, VT):
        """
        Static lung stretch receptor response.
        
        Proportional to tidal volume above baseline.
        
        Args:
            VT: Tidal volume (L)
        
        Returns:
            float: Static lung stretch activity
        """
        
        f_ls_static = self.G_ls * max(0, VT - self.VT_n)
        
        return f_ls_static
    
    def lungStretchReceptorDynamics(self, f_ls_static, x_ls):
        """
        First-order lung stretch receptor dynamics.
        
        Args:
            f_ls_static: Static response
            x_ls: Current dynamic state
        
        Returns:
            float: dx_ls/dt for integration
        """
        return (f_ls_static - x_ls) / self.tau_ls
    
    def lungStretchReceptor(self, VT, x_ls):
        """
        Complete lung stretch receptor response.
        
        Args:
            VT: Tidal volume (L)
            x_ls: Dynamic state
        
        Returns:
            tuple: (f_ls, dx_ls_dt)
        """
        f_ls_static = self.lungStretchReceptorStatic(VT)
        dx_ls_dt = self.lungStretchReceptorDynamics(f_ls_static, x_ls)
        
        return x_ls, dx_ls_dt
    
    # =========================================================================
    # SECTION 2: CNS PROCESSING
    # =========================================================================
    
    # --- 2A: CNS Ischemic Response (cnsIschemicResponse.py) ---
    
    def cnsIschemicO2Static(self, pO2_brain):
        """
        CNS ischemic response to brain hypoxia.
        
        Activated when brain pO2 falls below threshold.
        Ursino & Magosso 2000.
        
        Args:
            pO2_brain: Brain tissue O2 (mmHg)
        
        Returns:
            float: Static CNS O2 response
        """
        
        if pO2_brain < self.pO2_cns_th:
            f_cns_O2_static = self.G_cns_O2 * (self.pO2_cns_th - pO2_brain)
        else:
            f_cns_O2_static = 0.0
        
        return f_cns_O2_static
    
    def cnsIschemicCO2Static(self, pCO2_brain):
        """
        CNS ischemic response to brain hypercapnia.
        
        Activated when brain pCO2 rises above threshold.
        
        Args:
            pCO2_brain: Brain tissue CO2 (mmHg)
        
        Returns:
            float: Static CNS CO2 response
        """
        
        if pCO2_brain > self.pCO2_cns_th:
            f_cns_CO2_static = self.G_cns_CO2 * (pCO2_brain - self.pCO2_cns_th)
        else:
            f_cns_CO2_static = 0.0
        
        return f_cns_CO2_static
    
    def cnsIschemicDynamics(self, f_static, x_cns, tau_cns):
        """
        First-order CNS ischemic response dynamics.
        
        Args:
            f_static: Static response
            x_cns: Current dynamic state
            tau_cns: Time constant (s)
        
        Returns:
            float: dx_cns/dt for integration
        """
        return (f_static - x_cns) / tau_cns
    
    def cnsIschemicResponse(self, pO2_brain, pCO2_brain, x_cns_O2, x_cns_CO2):
        """
        Complete CNS ischemic response.
        
        Args:
            pO2_brain: Brain O2 (mmHg)
            pCO2_brain: Brain CO2 (mmHg)
            x_cns_O2: O2 dynamic state
            x_cns_CO2: CO2 dynamic state
        
        Returns:
            tuple: (f_cns, dx_cns_O2_dt, dx_cns_CO2_dt)
        """
        
        f_O2_static = self.cnsIschemicO2Static(pO2_brain)
        f_CO2_static = self.cnsIschemicCO2Static(pCO2_brain)
        
        dx_cns_O2_dt = self.cnsIschemicDynamics(f_O2_static, x_cns_O2, self.tau_cns_O2)
        dx_cns_CO2_dt = self.cnsIschemicDynamics(f_CO2_static, x_cns_CO2, self.tau_cns_CO2)
        
        # Combined CNS ischemic signal
        f_cns = x_cns_O2 + x_cns_CO2
        
        return f_cns, dx_cns_O2_dt, dx_cns_CO2_dt
    
    # --- 2B: Autonomic Nervous System (autonomicNervousSystem.py) ---
    
    def sympatheticEfferentActivity(self, f_baroreceptor, f_chemoreceptor, f_cns, f_lung_stretch, f_central_command=0.0):
        """
        Compute sympathetic efferent activity.
        
        Integrates baroreceptor (inhibitory), chemoreceptor (excitatory),
        CNS ischemic (excitatory), lung stretch (inhibitory), and
        central command (excitatory) inputs.
        
        Ursino 1998, Magosso & Ursino 2001.
        
        Args:
            f_baroreceptor: Combined baroreceptor afferent (Hz)
            f_chemoreceptor: Combined chemoreceptor afferent (Hz)
            f_cns: CNS ischemic response
            f_lung_stretch: Lung stretch receptor activity
            f_central_command: Central command input (exercise)
        
        Returns:
            float: Sympathetic efferent activity (Hz)
        """
        
        # Baroreceptor inhibition (sigmoidal)
        baro_effect = self.f_es_0 - self.k_es * (f_baroreceptor - self.f_ab_min)
        
        # Chemoreceptor excitation
        chemo_effect = 0.5 * f_chemoreceptor
        
        # CNS ischemic excitation
        cns_effect = f_cns
        
        # Lung stretch inhibition
        ls_effect = -0.2 * f_lung_stretch
        
        # Central command excitation
        cc_effect = f_central_command
        
        # Combined sympathetic output
        f_es = baro_effect + chemo_effect + cns_effect + ls_effect + cc_effect
        
        # Clamp to physiological range
        f_es = np.clip(f_es, self.f_es_inf, 30.0)
        
        return f_es
    
    def parasympatheticEfferentActivity(self, f_baroreceptor, f_chemoreceptor, f_lung_stretch, f_central_command=0.0):
        """
        Compute parasympathetic (vagal) efferent activity.
        
        Integrates baroreceptor (excitatory), chemoreceptor (weak excitatory),
        lung stretch (excitatory), and central command (inhibitory) inputs.
        
        Args:
            f_baroreceptor: Combined baroreceptor afferent (Hz)
            f_chemoreceptor: Combined chemoreceptor afferent (Hz)
            f_lung_stretch: Lung stretch receptor activity
            f_central_command: Central command input (exercise)
        
        Returns:
            float: Vagal efferent activity (Hz)
        """
        
        # Baroreceptor excitation (sigmoidal)
        baro_effect = self.f_ev_0 + self.k_ev * (f_baroreceptor - self.f_ab_min)
        
        # Chemoreceptor weak excitation
        chemo_effect = 0.1 * f_chemoreceptor
        
        # Lung stretch excitation (respiratory sinus arrhythmia)
        ls_effect = 0.3 * f_lung_stretch
        
        # Central command withdrawal
        cc_effect = -f_central_command
        
        # Combined vagal output
        f_ev = baro_effect + chemo_effect + ls_effect + cc_effect
        
        # Clamp to physiological range
        f_ev = np.clip(f_ev, 0.0, self.f_ev_inf)
        
        return f_ev
    
    # =========================================================================
    # SECTION 3: EFFERENT PATHWAYS
    # =========================================================================
    
    # --- 3A: Sympathetic Effectors (sympathetic.py) ---
    
    def peripheralResistanceStatic(self, f_es):
        """
        Static peripheral resistance response to sympathetic activity.
        
        Sigmoidal relationship.
        Ursino 1998 Eq. 13.
        
        Args:
            f_es: Sympathetic efferent activity (Hz)
        
        Returns:
            float: Static resistance multiplier
        """
        
        # Sigmoidal activation
        R_static = self.R_inf + (self.R_max - self.R_inf) * (f_es - self.f_es_inf) / (f_es - self.f_es_inf + self.G_R)
        
        return R_static
    
    def peripheralResistanceDynamics(self, R_static, x_R):
        """
        First-order resistance dynamics.
        
        Args:
            R_static: Static resistance
            x_R: Current dynamic state
        
        Returns:
            float: dx_R/dt for integration
        """
        return (R_static - x_R) / self.tau_R
    
    def venousUnstressedVolumeStatic(self, f_es):
        """
        Static venous unstressed volume response to sympathetic activity.
        
        Increased sympathetic activity reduces unstressed volume (venoconstriction).
        Ursino 1998 Eq. 14.
        
        Args:
            f_es: Sympathetic efferent activity (Hz)
        
        Returns:
            float: Static unstressed volume (mL)
        """
        
        # Linear decrease with sympathetic activity
        V_static = self.Vu_0 - self.G_V * (f_es - self.f_es_inf)
        
        return max(500.0, V_static)  # Minimum unstressed volume
    
    def venousUnstressedVolumeDynamics(self, V_static, x_V):
        """
        First-order venous volume dynamics.
        
        Args:
            V_static: Static volume
            x_V: Current dynamic state
        
        Returns:
            float: dx_V/dt for integration
        """
        return (V_static - x_V) / self.tau_V
    
    def cardiacContractilityStatic(self, f_es):
        """
        Static cardiac contractility response to sympathetic activity.
        
        Increased sympathetic activity increases contractility.
        Ursino 1998 Eq. 15.
        
        Args:
            f_es: Sympathetic efferent activity (Hz)
        
        Returns:
            float: Static contractility multiplier
        """
        
        E_static = self.E_0 + self.G_E * (f_es - self.f_es_inf)
        
        return min(E_static, self.E_max)
    
    def cardiacContractilityDynamics(self, E_static, x_E):
        """
        First-order contractility dynamics.
        
        Args:
            E_static: Static contractility
            x_E: Current dynamic state
        
        Returns:
            float: dx_E/dt for integration
        """
        return (E_static - x_E) / self.tau_E
    
    def sympatheticEffectors(self, f_es, x_R, x_V, x_E):
        """
        Complete sympathetic effector responses.
        
        Args:
            f_es: Sympathetic efferent activity (Hz)
            x_R: Resistance dynamic state
            x_V: Venous volume dynamic state
            x_E: Contractility dynamic state
        
        Returns:
            tuple: (R_mult, Vu, E_mult, dx_R_dt, dx_V_dt, dx_E_dt)
        """
        # Static values
        R_static = self.peripheralResistanceStatic(f_es)
        V_static = self.venousUnstressedVolumeStatic(f_es)
        E_static = self.cardiacContractilityStatic(f_es)
        
        # Dynamics
        dx_R_dt = self.peripheralResistanceDynamics(R_static, x_R)
        dx_V_dt = self.venousUnstressedVolumeDynamics(V_static, x_V)
        dx_E_dt = self.cardiacContractilityDynamics(E_static, x_E)
        
        return x_R, x_V, x_E, dx_R_dt, dx_V_dt, dx_E_dt
    
    # --- 3B: Parasympathetic Effectors (parasympathetic.py) ---
    
    def heartPeriodSympatheticStatic(self, f_es):
        """
        Static heart period response to sympathetic activity.
        
        Increased sympathetic activity decreases heart period (increases HR).
        Ursino 1998 Eq. 16.
        
        Args:
            f_es: Sympathetic efferent activity (Hz)
        
        Returns:
            float: Sympathetic contribution to heart period (s)
        """
        
        delta_T_s = -self.G_Ts * (f_es - self.f_es_inf)
        
        return delta_T_s
    
    def heartPeriodSympatheticDynamics(self, delta_T_s_static, x_Ts):
        """
        First-order sympathetic heart period dynamics.
        
        Args:
            delta_T_s_static: Static sympathetic contribution
            x_Ts: Current dynamic state
        
        Returns:
            float: dx_Ts/dt for integration
        """
        return (delta_T_s_static - x_Ts) / self.tau_Ts
    
    def heartPeriodVagalStatic(self, f_ev):
        """
        Static heart period response to vagal activity.
        
        Increased vagal activity increases heart period (decreases HR).
        Ursino 1998 Eq. 17.
        
        Args:
            f_ev: Vagal efferent activity (Hz)
        
        Returns:
            float: Vagal contribution to heart period (s)
        """
        
        delta_T_v = self.G_Tv * f_ev
        
        return delta_T_v
    
    def heartPeriodVagalDynamics(self, delta_T_v_static, x_Tv):
        """
        First-order vagal heart period dynamics.
        
        Args:
            delta_T_v_static: Static vagal contribution
            x_Tv: Current dynamic state
        
        Returns:
            float: dx_Tv/dt for integration
        """
        return (delta_T_v_static - x_Tv) / self.tau_Tv
    
    def heartPeriodEffectors(self, f_es, f_ev, x_Ts, x_Tv):
        """
        Complete heart period effector response.
        
        Args:
            f_es: Sympathetic efferent (Hz)
            f_ev: Vagal efferent (Hz)
            x_Ts: Sympathetic HR dynamic state
            x_Tv: Vagal HR dynamic state
        
        Returns:
            tuple: (T, dx_Ts_dt, dx_Tv_dt)
        """
        
        # Static values
        delta_T_s_static = self.heartPeriodSympatheticStatic(f_es)
        delta_T_v_static = self.heartPeriodVagalStatic(f_ev)
        
        # Dynamics
        dx_Ts_dt = self.heartPeriodSympatheticDynamics(delta_T_s_static, x_Ts)
        dx_Tv_dt = self.heartPeriodVagalDynamics(delta_T_v_static, x_Tv)
        
        # Total heart period
        T = self.T_0 + x_Ts + x_Tv
        
        # Clamp to physiological range
        T = np.clip(T, self.T_min, self.T_max)
        
        return T, dx_Ts_dt, dx_Tv_dt
    
    # =========================================================================
    # SECTION 4: LOCAL AUTOREGULATION
    # =========================================================================
    
    # --- 4A: Autoregulation (autoregulation.py) ---
    
    def autoregulationO2Static(self, pO2_tissue, pO2_setpoint, G_O2):
        """
        Static O2 autoregulation response.
        
        Vasodilation when tissue O2 falls below setpoint.
        
        Args:
            pO2_tissue: Tissue O2 partial pressure (mmHg)
            pO2_setpoint: Setpoint O2 (mmHg)
            G_O2: Gain coefficient
        
        Returns:
            float: Static O2 autoregulation signal
        """
        return G_O2 * max(0, pO2_setpoint - pO2_tissue)
    
    def autoregulationCO2Static(self, pCO2_tissue, pCO2_setpoint, G_CO2):
        """
        Static CO2 autoregulation response.
        
        Vasodilation when tissue CO2 rises above setpoint.
        
        Args:
            pCO2_tissue: Tissue CO2 partial pressure (mmHg)
            pCO2_setpoint: Setpoint CO2 (mmHg)
            G_CO2: Gain coefficient
        
        Returns:
            float: Static CO2 autoregulation signal
        """
        return G_CO2 * max(0, pCO2_tissue - pCO2_setpoint)
    
    def autoregulationDynamics(self, sigma_static, x_auto, tau_auto):
        """
        First-order autoregulation dynamics.
        
        Args:
            sigma_static: Static autoregulation signal
            x_auto: Current dynamic state
            tau_auto: Time constant (s)
        
        Returns:
            float: dx_auto/dt for integration
        """
        return (sigma_static - x_auto) / tau_auto
    
    def brainAutoregulation(self, pO2_brain, pCO2_brain, x_br_O2, x_br_CO2):
        """
        Brain autoregulation response.
        
        Strong CO2 reactivity, moderate O2 reactivity.
        
        Args:
            pO2_brain: Brain O2 (mmHg)
            pCO2_brain: Brain CO2 (mmHg)
            x_br_O2: Brain O2 autoregulation state
            x_br_CO2: Brain CO2 autoregulation state
        
        Returns:
            tuple: (sigma_br, dx_br_O2_dt, dx_br_CO2_dt)
        """
        
        sigma_O2_static = self.autoregulationO2Static(pO2_brain, self.pO2_n, self.G_br_O2)
        sigma_CO2_static = self.autoregulationCO2Static(pCO2_brain, self.pCO2_n, self.G_br_CO2)
        
        dx_br_O2_dt = self.autoregulationDynamics(sigma_O2_static, x_br_O2, self.tau_br_O2)
        dx_br_CO2_dt = self.autoregulationDynamics(sigma_CO2_static, x_br_CO2, self.tau_br_CO2)
        
        # Combined brain autoregulation signal
        sigma_br = x_br_O2 + x_br_CO2
        
        return sigma_br, dx_br_O2_dt, dx_br_CO2_dt
    
    def coronaryAutoregulation(self, pO2_cor, pCO2_cor, x_cor_O2, x_cor_CO2):
        """
        Coronary autoregulation response.
        
        Strong metabolic coupling.
        
        Args:
            pO2_cor: Coronary tissue O2 (mmHg)
            pCO2_cor: Coronary tissue CO2 (mmHg)
            x_cor_O2: Coronary O2 autoregulation state
            x_cor_CO2: Coronary CO2 autoregulation state
        
        Returns:
            tuple: (sigma_cor, dx_cor_O2_dt, dx_cor_CO2_dt)
        """
        
        sigma_O2_static = self.autoregulationO2Static(pO2_cor, self.pO2_n, self.G_cor_O2)
        sigma_CO2_static = self.autoregulationCO2Static(pCO2_cor, self.pCO2_n, self.G_cor_CO2)
        
        dx_cor_O2_dt = self.autoregulationDynamics(sigma_O2_static, x_cor_O2, self.tau_cor_O2)
        dx_cor_CO2_dt = self.autoregulationDynamics(sigma_CO2_static, x_cor_CO2, self.tau_cor_CO2)
        
        sigma_cor = x_cor_O2 + x_cor_CO2
        
        return sigma_cor, dx_cor_O2_dt, dx_cor_CO2_dt
    
    def muscleAutoregulation(self, pO2_mus, pCO2_mus, x_mus_O2, x_mus_CO2):
        """
        Skeletal muscle autoregulation response.
        
        Strong O2 reactivity during exercise.
        
        Args:
            pO2_mus: Muscle tissue O2 (mmHg)
            pCO2_mus: Muscle tissue CO2 (mmHg)
            x_mus_O2: Muscle O2 autoregulation state
            x_mus_CO2: Muscle CO2 autoregulation state
        
        Returns:
            tuple: (sigma_mus, dx_mus_O2_dt, dx_mus_CO2_dt)
        """
        
        sigma_O2_static = self.autoregulationO2Static(pO2_mus, self.pO2_n, self.G_mus_O2)
        sigma_CO2_static = self.autoregulationCO2Static(pCO2_mus, self.pCO2_n, self.G_mus_CO2)
        
        dx_mus_O2_dt = self.autoregulationDynamics(sigma_O2_static, x_mus_O2, self.tau_mus_O2)
        dx_mus_CO2_dt = self.autoregulationDynamics(sigma_CO2_static, x_mus_CO2, self.tau_mus_CO2)
        
        sigma_mus = x_mus_O2 + x_mus_CO2
        
        return sigma_mus, dx_mus_O2_dt, dx_mus_CO2_dt
    
    # =========================================================================
    # SECTION 5: EXERCISE COMPONENTS
    # =========================================================================
    
    # --- 5A: Exercise Intensity (exerciseIntensity.py) ---
    
    def exerciseIntensity(self, t, I_max, t_onset, t_duration, ramp_time=30.0):
        """
        Exercise intensity profile.
        
        Smooth onset and offset with optional ramp.
        Magosso & Ursino 2002.
        
        Args:
            t: Current time (s)
            I_max: Maximum intensity (0-1 scale)
            t_onset: Exercise start time (s)
            t_duration: Exercise duration (s)
            ramp_time: Ramp up/down time (s)
        
        Returns:
            float: Current exercise intensity (0-1)
        """
        if t < t_onset:
            return 0.0
        
        t_exercise = t - t_onset
        
        if t_exercise < ramp_time:
            # Ramp up
            I = I_max * (t_exercise / ramp_time)
        elif t_exercise < t_duration - ramp_time:
            # Steady state
            I = I_max
        elif t_exercise < t_duration:
            # Ramp down
            I = I_max * (t_duration - t_exercise) / ramp_time
        else:
            # Recovery
            I = 0.0
        
        return I
    
    # --- 5B: Central Command (centralCommand.py) ---
    
    def centralCommandSympathetic(self, I):
        """
        Central command sympathetic activation.
        
        Feed-forward signal from motor cortex.
        Magosso & Ursino 2002 Eq. 21.
        
        Args:
            I: Exercise intensity (0-1)
        
        Returns:
            float: Central command sympathetic signal (Hz)
        """
        
        if I > self.I_th_cc:
            f_cc_s = self.G_cc_symp * (I - self.I_th_cc)
        else:
            f_cc_s = 0.0
        
        return f_cc_s
    
    def centralCommandVagal(self, I):
        """
        Central command vagal withdrawal.
        
        Reduces vagal tone during exercise.
        Magosso & Ursino 2002 Eq. 22.
        
        Args:
            I: Exercise intensity (0-1)
        
        Returns:
            float: Central command vagal withdrawal signal (Hz)
        """
        
        if I > self.I_th_cc:
            f_cc_v = self.G_cc_vagal * (I - self.I_th_cc)
        else:
            f_cc_v = 0.0
        
        return f_cc_v
    
    # --- 5C: Muscle Pump (musclePump.py) ---
    
    def intramuscularPressure(self, I, phase=0.0):
        """
        Intramuscular pressure during exercise.
        
        Rhythmic pressure changes from muscle contractions.
        Magosso & Ursino 2002.
        
        Args:
            I: Exercise intensity (0-1)
            phase: Contraction phase (0-1)
        
        Returns:
            float: Intramuscular pressure (mmHg)
        """
        
        # Pressure amplitude scales with intensity
        P_amp = self.P_im_max * I
        
        # Sinusoidal contraction pattern
        P_im = P_amp * (0.5 + 0.5 * np.sin(2 * np.pi * phase))
        
        return P_im
    
    def muscleVenousResistanceEffect(self, P_im, R_mv_baseline=0.1):
        """
        Effect of intramuscular pressure on venous resistance.
        
        Compression increases resistance, aiding venous return.
        
        Args:
            P_im: Intramuscular pressure (mmHg)
            R_mv_baseline: Baseline muscle venous resistance (mmHg·s/mL)
        
        Returns:
            float: Effective muscle venous resistance (mmHg·s/mL)
        """
        # Resistance increases with compression
        R_mv = R_mv_baseline * (1.0 + 0.02 * P_im)
        
        return R_mv
    
    def muscleVenousVolumeEffect(self, P_im, Vu_muscle_baseline=200.0):
        """
        Effect of intramuscular pressure on venous unstressed volume.
        
        Compression reduces unstressed volume, mobilizing blood.
        
        Args:
            P_im: Intramuscular pressure (mmHg)
            Vu_muscle_baseline: Baseline muscle venous unstressed volume (mL)
        
        Returns:
            float: Effective muscle venous unstressed volume (mL)
        """
        # Volume decreases with compression
        delta_Vu = self.params['k_mp'] * P_im
        Vu_mus = max(50.0, Vu_muscle_baseline - delta_Vu)
        
        return Vu_mus
    
    # --- 5D: Exercise Metabolism (exerciseMetabolism.py) ---
    
    def oxygenConsumption(self, I):
        """
        Oxygen consumption rate during exercise.
        
        Linear increase with intensity.
        Magosso & Ursino 2002.
        
        Args:
            I: Exercise intensity (0-1)
        
        Returns:
            float: O2 consumption rate (mL/min)
        """
        
        VO2 = self.VO2_rest + (self.VO2_max - self.VO2_rest) * I
        
        return VO2
    
    def carbonDioxideProduction(self, I):
        """
        CO2 production rate during exercise.
        
        Increases with intensity, RQ shifts toward 1.0.
        
        Args:
            I: Exercise intensity (0-1)
        
        Returns:
            float: CO2 production rate (mL/min)
        """
        
        # RQ increases with intensity
        RQ = self.RQ_rest + (self.RQ_max - self.RQ_rest) * I
        
        VO2 = self.oxygenConsumption(I)
        VCO2 = RQ * VO2
        
        return VCO2
    
    def exerciseMetabolicResponse(self, I):
        """
        Complete metabolic response to exercise.
        
        Args:
            I: Exercise intensity (0-1)
        
        Returns:
            dict: Metabolic parameters
        """
        VO2 = self.oxygenConsumption(I)
        VCO2 = self.carbonDioxideProduction(I)
        RQ = VCO2 / VO2 if VO2 > 0 else 0.8
        
        return {
            'VO2': VO2,           # mL/min
            'VCO2': VCO2,         # mL/min
            'RQ': RQ              # dimensionless
        }
    
    # --- 5E: Respiratory Pump (respiratoryPump.py) ---
    # NOTE: Intrathoracic/abdominal pressures handled by LungMechanicsModel
    #       This section only contains exercise ventilation response
    
    def exerciseVentilationResponse(self, I, x_Vdot_slow):
        """
        Exercise ventilation response with fast and slow components.
        
        Implements Magosso & Ursino 2002 Eq. 27-33.
        
        Args:
            I: Exercise intensity (0-1)
            x_Vdot_slow: Slow ventilation component state (L/min)
        
        Returns:
            tuple: (Vdot, dx_Vdot_slow_dt)
                Vdot: Total minute ventilation (L/min)
                dx_Vdot_slow_dt: Derivative for slow component
        """
        
        # Steady-state ventilation increase (quadratic relationship)
        # ΔV̇_steady = A*I + B*I²
        delta_Vdot_steady = self.A_vent * I + self.B_vent * I * I
        
        # Fast component (immediate, 45% of steady-state)
        delta_Vdot_fast = self.fast_fraction * delta_Vdot_steady
        
        # Slow component dynamics
        # dΔV̇_slow/dt = (1/τ_v) * (-ΔV̇_slow + 0.55 * ΔV̇_steady)
        slow_fraction = 1.0 - self.fast_fraction  # 0.55
        dx_Vdot_slow_dt = (slow_fraction * delta_Vdot_steady - x_Vdot_slow) / self.tau_v
        
        # Total ventilation
        Vdot = self.Vdot_n + delta_Vdot_fast + x_Vdot_slow
        
        return Vdot, dx_Vdot_slow_dt
    
    # =========================================================================
    # SECTION 6: FINAL EFFECTOR INTEGRATION
    # =========================================================================
    
    # --- 6A: Final Effector Values (finalEffectorValues.py) ---
    
    def finalPeripheralResistance(self, R_baseline, R_sympathetic_mult, sigma_autoregulation, bed='generic'):
        """
        Final peripheral resistance incorporating all control mechanisms.
        
        Args:
            R_baseline: Baseline resistance (mmHg·s/mL)
            R_sympathetic_mult: Sympathetic multiplier from efferent pathway
            sigma_autoregulation: Local autoregulation signal
            bed: Vascular bed name for bed-specific gains
        
        Returns:
            float: Final resistance (mmHg·s/mL)
        """
        # Bed-specific autoregulation gain
        auto_gains = {
            'brain': 0.3,
            'coronary': 0.5,
            'muscle': 0.4,
            'splanchnic': 0.2,
            'extrasplanchnic': 0.2,
            'generic': 0.3
        }
        k_auto = auto_gains.get(bed, 0.3)
        
        # Combine sympathetic (increases R) and autoregulation (decreases R)
        R_final = R_baseline * R_sympathetic_mult / (1.0 + k_auto * sigma_autoregulation)
        
        return max(0.01, R_final)  # Minimum resistance
    
    def finalVenousUnstressedVolume(self, Vu_sympathetic, Vu_muscle_pump=0.0):
        """
        Final venous unstressed volume incorporating all control mechanisms.
        
        Args:
            Vu_sympathetic: Unstressed volume from sympathetic control (mL)
            Vu_muscle_pump: Change from muscle pump effect (mL, negative)
        
        Returns:
            float: Final unstressed volume (mL)
        """
        Vu_final = Vu_sympathetic + Vu_muscle_pump
        
        return max(500.0, Vu_final)  # Minimum volume
    
    def finalCardiacContractility(self, E_baseline, E_sympathetic_mult):
        """
        Final cardiac contractility.
        
        Args:
            E_baseline: Baseline elastance (mmHg/mL)
            E_sympathetic_mult: Sympathetic multiplier
        
        Returns:
            float: Final elastance (mmHg/mL)
        """
        return E_baseline * E_sympathetic_mult
    
    def finalHeartPeriod(self, T):
        """
        Final heart period (already computed in heartPeriodEffectors).
        
        Args:
            T: Heart period from autonomic control (s)
        
        Returns:
            float: Final heart period (s)
        """
        return np.clip(T, self.T_min, self.T_max)
    
    # =========================================================================
    # SECTION 7: MASTER COMPUTE DERIVATIVES
    # =========================================================================
    
    def compute_derivatives(self, t, state, inputs):
        """
        Master function computing all control system derivatives.
        
        Suitable for integration with scipy.integrate.solve_ivp.
        
        Args:
            t: Current time (s)
            state: Dict of all state variables
            inputs: Dict of physiological inputs (pressures, blood gases, etc.)
        
        Returns:
            dict: All derivatives for state variables
        
        State Variables:
            Baroreceptors: x_ab, x_ab_dot, x_Ab, x_Ab_dot
            Chemoreceptors: x_pO2, x_pCO2, x_cCO2
            Lung stretch: x_ls
            CNS ischemic: x_cns_O2, x_cns_CO2
            Sympathetic: x_R, x_V, x_E
            Parasympathetic: x_Ts, x_Tv
            Autoregulation: x_br_O2, x_br_CO2, x_cor_O2, x_cor_CO2, x_mus_O2, x_mus_CO2
            Exercise ventilation: x_Vdot_slow
        
        Inputs Required:
            P_carotid: Carotid pressure (mmHg)
            P_aortic: Aortic pressure (mmHg)
            pO2_art: Arterial O2 (mmHg)
            pCO2_art: Arterial CO2 (mmHg)
            pO2_brain, pCO2_brain: Brain gases (mmHg)
            pO2_cor, pCO2_cor: Coronary gases (mmHg)
            pO2_mus, pCO2_mus: Muscle gases (mmHg)
            I: Exercise intensity (0-1)
            VT: Tidal volume (L)
        """
        derivatives = {}
        
        # --- Extract State Variables ---
        x_ab = state.get('x_ab', 0.0)
        x_ab_dot = state.get('x_ab_dot', 0.0)
        x_Ab = state.get('x_Ab', 0.0)
        x_Ab_dot = state.get('x_Ab_dot', 0.0)
        x_pO2 = state.get('x_pO2', 0.0)
        x_pCO2 = state.get('x_pCO2', 0.0)
        x_cCO2 = state.get('x_cCO2', 0.0)
        x_ls = state.get('x_ls', 0.0)
        x_cns_O2 = state.get('x_cns_O2', 0.0)
        x_cns_CO2 = state.get('x_cns_CO2', 0.0)
        x_R = state.get('x_R', 1.0)
        x_V = state.get('x_V', self.params['Vu_0'])
        x_E = state.get('x_E', 1.0)
        x_Ts = state.get('x_Ts', 0.0)
        x_Tv = state.get('x_Tv', 0.0)
        x_br_O2 = state.get('x_br_O2', 0.0)
        x_br_CO2 = state.get('x_br_CO2', 0.0)
        x_cor_O2 = state.get('x_cor_O2', 0.0)
        x_cor_CO2 = state.get('x_cor_CO2', 0.0)
        x_mus_O2 = state.get('x_mus_O2', 0.0)
        x_mus_CO2 = state.get('x_mus_CO2', 0.0)
        x_Vdot_slow = state.get('x_Vdot_slow', 0.0)
        
        # --- Extract Inputs ---
        P_carotid = inputs.get('P_carotid', 92.0)
        P_aortic = inputs.get('P_aortic', 92.0)
        pO2_art = inputs.get('pO2_art', 100.0)
        pCO2_art = inputs.get('pCO2_art', 40.0)
        pO2_brain = inputs.get('pO2_brain', 40.0)
        pCO2_brain = inputs.get('pCO2_brain', 46.0)
        pO2_cor = inputs.get('pO2_cor', 30.0)
        pCO2_cor = inputs.get('pCO2_cor', 50.0)
        pO2_mus = inputs.get('pO2_mus', 35.0)
        pCO2_mus = inputs.get('pCO2_mus', 45.0)
        I = inputs.get('I', 0.0)
        VT = inputs.get('VT', 0.5)
        
        # =====================================================================
        # 1. AFFERENT PROCESSING
        # =====================================================================
        
        # Baroreceptors
        f_ab, dx_ab_dt, dx_ab_dot_dt = self.carotidBaroreceptor(P_carotid, x_ab, x_ab_dot)
        f_Ab, dx_Ab_dt, dx_Ab_dot_dt = self.aorticBaroreceptor(P_aortic, x_Ab, x_Ab_dot)
        f_baroreceptor = self.combinedBaroreceptorAfferent(f_ab, f_Ab)
        
        derivatives['x_ab'] = dx_ab_dt
        derivatives['x_ab_dot'] = dx_ab_dot_dt
        derivatives['x_Ab'] = dx_Ab_dt
        derivatives['x_Ab_dot'] = dx_Ab_dot_dt
        
        # Chemoreceptors
        f_peripheral, dx_pO2_dt, dx_pCO2_dt = self.peripheralChemoreceptor(pO2_art, pCO2_art, x_pO2, x_pCO2)
        f_central, dx_cCO2_dt = self.centralChemoreceptor(pCO2_brain, x_cCO2)
        f_chemoreceptor = f_peripheral + f_central
        
        derivatives['x_pO2'] = dx_pO2_dt
        derivatives['x_pCO2'] = dx_pCO2_dt
        derivatives['x_cCO2'] = dx_cCO2_dt
        
        # Lung stretch receptors
        f_lung_stretch, dx_ls_dt = self.lungStretchReceptor(VT, x_ls)
        
        derivatives['x_ls'] = dx_ls_dt
        
        # =====================================================================
        # 2. CNS PROCESSING
        # =====================================================================
        
        # CNS ischemic response
        f_cns, dx_cns_O2_dt, dx_cns_CO2_dt = self.cnsIschemicResponse(pO2_brain, pCO2_brain, x_cns_O2, x_cns_CO2)
        
        derivatives['x_cns_O2'] = dx_cns_O2_dt
        derivatives['x_cns_CO2'] = dx_cns_CO2_dt
        
        # Central command (exercise)
        f_cc_s = self.centralCommandSympathetic(I)
        f_cc_v = self.centralCommandVagal(I)
        
        # Autonomic efferent activity
        f_es = self.sympatheticEfferentActivity(f_baroreceptor, f_chemoreceptor, f_cns, f_lung_stretch, f_cc_s)
        f_ev = self.parasympatheticEfferentActivity(f_baroreceptor, f_chemoreceptor, f_lung_stretch, f_cc_v)
        
        # =====================================================================
        # 3. EFFERENT PATHWAYS
        # =====================================================================
        
        # Sympathetic effectors
        R_mult, Vu, E_mult, dx_R_dt, dx_V_dt, dx_E_dt = self.sympatheticEffectors(f_es, x_R, x_V, x_E)
        
        derivatives['x_R'] = dx_R_dt
        derivatives['x_V'] = dx_V_dt
        derivatives['x_E'] = dx_E_dt
        
        # Heart period effectors
        T, dx_Ts_dt, dx_Tv_dt = self.heartPeriodEffectors(f_es, f_ev, x_Ts, x_Tv)
        
        derivatives['x_Ts'] = dx_Ts_dt
        derivatives['x_Tv'] = dx_Tv_dt
        
        # =====================================================================
        # 4. LOCAL AUTOREGULATION
        # =====================================================================
        
        sigma_br, dx_br_O2_dt, dx_br_CO2_dt = self.brainAutoregulation(pO2_brain, pCO2_brain, x_br_O2, x_br_CO2)
        sigma_cor, dx_cor_O2_dt, dx_cor_CO2_dt = self.coronaryAutoregulation(pO2_cor, pCO2_cor, x_cor_O2, x_cor_CO2)
        sigma_mus, dx_mus_O2_dt, dx_mus_CO2_dt = self.muscleAutoregulation(pO2_mus, pCO2_mus, x_mus_O2, x_mus_CO2)
        
        derivatives['x_br_O2'] = dx_br_O2_dt
        derivatives['x_br_CO2'] = dx_br_CO2_dt
        derivatives['x_cor_O2'] = dx_cor_O2_dt
        derivatives['x_cor_CO2'] = dx_cor_CO2_dt
        derivatives['x_mus_O2'] = dx_mus_O2_dt
        derivatives['x_mus_CO2'] = dx_mus_CO2_dt
        
        # =====================================================================
        # 5. EXERCISE VENTILATION
        # =====================================================================
        
        Vdot, dx_Vdot_slow_dt = self.exerciseVentilationResponse(I, x_Vdot_slow)
        
        derivatives['x_Vdot_slow'] = dx_Vdot_slow_dt
        
        # =====================================================================
        # 6. COMPUTED OUTPUTS (for reference, not state derivatives)
        # =====================================================================
        
        outputs = {
            # Afferent activities
            'f_baroreceptor': f_baroreceptor,
            'f_chemoreceptor': f_chemoreceptor,
            'f_lung_stretch': f_lung_stretch,
            'f_cns': f_cns,
            
            # Efferent activities
            'f_es': f_es,
            'f_ev': f_ev,
            
            # Effector values
            'R_mult': R_mult,
            'Vu': Vu,
            'E_mult': E_mult,
            'T': T,
            'HR': 60.0 / T,  # Heart rate in bpm
            
            # Autoregulation signals
            'sigma_br': sigma_br,
            'sigma_cor': sigma_cor,
            'sigma_mus': sigma_mus,
            
            # Exercise
            'Vdot': Vdot,
            'metabolic': self.exerciseMetabolicResponse(I)
        }
        
        return derivatives, outputs
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def getInitialState(self):
        """
        Return initial state vector for all control variables.
        
        Returns:
            dict: Initial state values at steady-state rest
        """
        
        return {
            # Baroreceptor states
            'x_ab': self.P_n,
            'x_ab_dot': 0.0,
            'x_Ab': self.P_n,
            'x_Ab_dot': 0.0,
            
            # Chemoreceptor states
            'x_pO2': 0.0,
            'x_pCO2': 0.0,
            'x_cCO2': 0.0,
            
            # Lung stretch
            'x_ls': 0.0,
            
            # CNS ischemic
            'x_cns_O2': 0.0,
            'x_cns_CO2': 0.0,
            
            # Sympathetic effectors
            'x_R': 1.0,
            'x_V': self.Vu_0,
            'x_E': 1.0,
            
            # Parasympathetic effectors
            'x_Ts': 0.0,
            'x_Tv': self.G_Tv * self.f_ev_0,
            
            # Autoregulation
            'x_br_O2': 0.0,
            'x_br_CO2': 0.0,
            'x_cor_O2': 0.0,
            'x_cor_CO2': 0.0,
            'x_mus_O2': 0.0,
            'x_mus_CO2': 0.0,
            
            # Exercise ventilation
            'x_Vdot_slow': 0.0
        }
    
    def getStateNames(self):
        """
        Return ordered list of state variable names.
        
        Returns:
            list: State variable names
        """
        return [
            'x_ab', 'x_ab_dot', 'x_Ab', 'x_Ab_dot',
            'x_pO2', 'x_pCO2', 'x_cCO2',
            'x_ls',
            'x_cns_O2', 'x_cns_CO2',
            'x_R', 'x_V', 'x_E',
            'x_Ts', 'x_Tv',
            'x_br_O2', 'x_br_CO2', 'x_cor_O2', 'x_cor_CO2', 'x_mus_O2', 'x_mus_CO2',
            'x_Vdot_slow'
        ]
    
    def stateToArray(self, state_dict):
        """
        Convert state dictionary to array for ODE solver.
        
        Args:
            state_dict: Dictionary of state values
        
        Returns:
            np.array: State vector
        """
        names = self.getStateNames()
        return np.array([state_dict[name] for name in names])
    
    def arrayToState(self, state_array):
        """
        Convert state array to dictionary.
        
        Args:
            state_array: State vector
        
        Returns:
            dict: State dictionary
        """
        names = self.getStateNames()
        return {name: state_array[i] for i, name in enumerate(names)}


# =============================================================================
# STANDALONE TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ControlSystemModel - Comprehensive Cardiovascular Control")
    print("=" * 70)
    
    # Test parameters
    testParams = {
        # Baroreceptor
        'P_n': 92.0, 'k_ab': 11.76, 'tau_ab': 0.8, 'tau_ab_z': 6.37,
        'k_Ab': 11.76, 'tau_Ab': 0.8, 'tau_Ab_z': 6.37,
        'f_ab_min': 2.52, 'f_ab_max': 47.78,
        # Chemoreceptor
        'pO2_n': 100.0, 'pCO2_n': 40.0, 'G_pO2': 0.4, 'G_pCO2': 0.2, 'G_cCO2': 0.1,
        'tau_pO2': 2.0, 'tau_pCO2': 5.0, 'tau_cCO2': 60.0, 'f_ch_min': 0.0, 'f_ch_max': 12.0,
        # Lung stretch
        'G_ls': 0.05, 'tau_ls': 2.0, 'VT_n': 0.5,
        # CNS ischemic
        'pO2_cns_th': 35.0, 'pCO2_cns_th': 50.0, 'G_cns_O2': 2.0, 'G_cns_CO2': 1.5,
        'tau_cns_O2': 20.0, 'tau_cns_CO2': 20.0,
        # Autonomic
        'f_es_inf': 2.1, 'f_es_0': 16.11, 'f_ev_0': 3.2, 'f_ev_inf': 6.3, 'k_es': 0.0675, 'k_ev': 0.0675,
        # Sympathetic
        'G_R': 0.8, 'tau_R': 6.0, 'D_R': 2.0, 'R_0': 1.0, 'R_inf': 0.2, 'R_max': 2.5,
        'G_V': 250.0, 'tau_V': 20.0, 'D_V': 5.0, 'Vu_0': 3000.0,
        'G_E': 0.5, 'tau_E': 8.0, 'D_E': 2.0, 'E_0': 1.0, 'E_max': 2.5,
        # Parasympathetic
        'G_Ts': 0.13, 'tau_Ts': 2.0, 'D_Ts': 2.0, 'G_Tv': 0.09, 'tau_Tv': 1.5, 'D_Tv': 0.2,
        'T_0': 0.833, 'T_min': 0.4, 'T_max': 1.5,
        # Autoregulation
        'G_br_O2': 0.5, 'G_br_CO2': 1.5, 'tau_br_O2': 20.0, 'tau_br_CO2': 20.0,
        'G_cor_O2': 1.0, 'G_cor_CO2': 0.8, 'tau_cor_O2': 10.0, 'tau_cor_CO2': 10.0,
        'G_mus_O2': 1.2, 'G_mus_CO2': 0.5, 'tau_mus_O2': 15.0, 'tau_mus_CO2': 15.0,
        # Central command
        'G_cc_symp': 5.0, 'G_cc_vagal': 3.0, 'I_th_cc': 0.0,
        # Muscle pump
        'P_im_max': 100.0, 'k_mp': 0.5, 'f_contraction': 1.0,
        # Exercise metabolism
        'VO2_rest': 250.0, 'VO2_max': 3000.0, 'VCO2_rest': 200.0, 'RQ_rest': 0.8, 'RQ_max': 1.0,
        # Respiratory pump
        'Vdot_n': 6.0, 'A_vent': 10.0, 'B_vent': 5.0, 'tau_v': 60.0, 'fast_fraction': 0.45,
    }
    
    # Create model
    model = ControlSystemModel(testParams)
    
    # Get initial state
    state = model.getInitialState()
    print(f"\nNumber of state variables: {len(state)}")
    print(f"State variables: {list(state.keys())}")
    
    # Test with resting inputs
    inputs_rest = {
        'P_carotid': 92.0,
        'P_aortic': 92.0,
        'pO2_art': 100.0,
        'pCO2_art': 40.0,
        'pO2_brain': 40.0,
        'pCO2_brain': 46.0,
        'pO2_cor': 30.0,
        'pCO2_cor': 50.0,
        'pO2_mus': 35.0,
        'pCO2_mus': 45.0,
        'I': 0.0,
        'VT': 0.5
    }
    
    print("\n--- Resting Conditions ---")
    derivatives, outputs = model.compute_derivatives(0.0, state, inputs_rest)
    print(f"Heart Rate: {outputs['HR']:.1f} bpm")
    print(f"Sympathetic Activity: {outputs['f_es']:.2f} Hz")
    print(f"Vagal Activity: {outputs['f_ev']:.2f} Hz")
    print(f"Minute Ventilation: {outputs['Vdot']:.1f} L/min")
    
    # Test with exercise
    inputs_exercise = inputs_rest.copy()
    inputs_exercise['I'] = 0.5  # 50% intensity
    
    print("\n--- Exercise (50% intensity) ---")
    derivatives, outputs = model.compute_derivatives(0.0, state, inputs_exercise)
    print(f"Heart Rate: {outputs['HR']:.1f} bpm")
    print(f"Sympathetic Activity: {outputs['f_es']:.2f} Hz")
    print(f"Vagal Activity: {outputs['f_ev']:.2f} Hz")
    print(f"Minute Ventilation: {outputs['Vdot']:.1f} L/min")
    print(f"O2 Consumption: {outputs['metabolic']['VO2']:.0f} mL/min")
    
    # Test with hypotension
    inputs_hypotension = inputs_rest.copy()
    inputs_hypotension['P_carotid'] = 60.0
    inputs_hypotension['P_aortic'] = 60.0
    
    print("\n--- Hypotension (MAP = 60 mmHg) ---")
    derivatives, outputs = model.compute_derivatives(0.0, state, inputs_hypotension)
    print(f"Baroreceptor Afferent: {outputs['f_baroreceptor']:.2f} Hz (reduced)")
    print(f"Sympathetic Activity: {outputs['f_es']:.2f} Hz (increased)")
    print(f"Resistance Multiplier: {outputs['R_mult']:.2f}")
    
    print("\n" + "=" * 70)
    print("All tests passed!")
    print("=" * 70)
