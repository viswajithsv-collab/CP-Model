import numpy as np


class LungMechanicsModel:
    """
    Lung Mechanics Model - Albanese 2016 Equations A30-A41

    Handles respiratory mechanics including:
    - Upper airways: larynx, trachea (A30-A31)
    - Lower airways: bronchea, alveoli (A32-A33)
    - Chest wall and pleural pressure (A34)
    - Flows (A35-A36)
    - Volumes (A37-A41)
    - Respiratory muscle pressure patterns (Eq 4)
    - Exercise effects on respiration (Magosso & Ursino 2002)
    """

    def __init__(self, params):
        """
        Initialize lung mechanics model

        Parameters dict should contain:
        - Resistances: Rml, Rlt, Rtb, RbA
        - Compliances: Cl, Ct, Cb, CA, Ccw
        - Unstressed volumes: Vu_l, Vu_tr, Vu_b, Vu_A (or FRC to calculate Vu_A)
        - Respiratory timing: RR (respiratory rate), IE (I/E ratio)
        - Muscle pressure: Pmus_min
        - Exercise: exercise_intensity, gthor, gabd, delta_VT
        - Pressure extremes: Pthor_min_n, Pthor_max_n, Pabd_min_n, Pabd_max_n
        - Initial states: Pl_init, Pt_init, Pb_init, PA_init, Ppl_init, Pmus_init
        """
        # Store parameters
        self.params = params

        # Resistances
        self.Rml = params['Rml']  # Mouth to larynx
        self.Rlt = params['Rlt']  # Larynx to trachea
        self.Rtb = params['Rtb']  # Trachea to bronchea
        self.RbA = params['RbA']  # Bronchea to alveoli

        # Compliances
        self.Cl = params['Cl']  # Larynx
        self.Ct = params['Ct']  # Trachea
        self.Cb = params['Cb']  # Bronchea
        self.CA = params['CA']  # Alveoli
        self.Ccw = params['Ccw']  # Chest wall

        # Unstressed volumes
        self.Vu_l = params['Vu_l']
        self.Vu_tr = params['Vu_tr']
        self.Vu_b = params['Vu_b']

        # Calculate Vu_A from FRC if provided (Equation 6)
        if 'FRC' in params:
            self.FRC = params['FRC']
            P_pl_EE = params.get('P_pl_EE', 0.0)
            V_l_EE = params.get('V_l_EE', 0.0)
            V_t_EE = params.get('V_t_EE', 0.0)
            V_b_EE = params.get('V_b_EE', 0.0)
            self.Vu_A = self.calculateVuA(self.FRC, self.CA, P_pl_EE, V_l_EE, V_t_EE, V_b_EE)
        else:
            self.Vu_A = params['Vu_A']

        # Respiratory timing
        self.RR = params['RR']  # Respiratory rate (breaths/min)
        self.IE = params['IE']  # I/E ratio

        # Muscle pressure
        self.Pmus_min = params['Pmus_min']

        # Exercise parameters
        self.exercise_intensity = params.get('exercise_intensity', 0.0)
        self.gthor = params.get('gthor', 0.0)
        self.gabd = params.get('gabd', 0.0)
        self.delta_VT = params.get('delta_VT', 0.0)

        # Baseline pressure extremes
        self.Pthor_min_n = params.get('Pthor_min_n', -5.0)
        self.Pthor_max_n = params.get('Pthor_max_n', -2.0)
        self.Pabd_min_n = params.get('Pabd_min_n', 0.0)
        self.Pabd_max_n = params.get('Pabd_max_n', 2.0)

        # Initialize state variables
        self.Pl = params.get('Pl_init', 0.0)  # Larynx pressure
        self.Pt = params.get('Pt_init', 0.0)  # Trachea pressure
        self.Pb = params.get('Pb_init', 0.0)  # Bronchea pressure
        self.PA = params.get('PA_init', 0.0)  # Alveolar pressure
        self.Ppl = params.get('Ppl_init', -5.0)  # Pleural pressure
        self.Pmus = params.get('Pmus_init', 0.0)  # Muscle pressure

        # Respiratory timing state
        self.b = 0.0  # Current phase time
        self.Ti = 0.0  # Inspiration time
        self.Te = 0.0  # Expiration time
        self.tau = 0.0  # Muscle pressure time constant

    def calculateVuA(self, FRC, CA, P_pl_EE, V_l_EE, V_t_EE, V_b_EE):
        """
        Calculate alveolar unstressed volume from FRC (Equation 6)
        Vu,A = FRC + CA * Ppl,EE - Vl,EE - Vt,EE - Vb,EE
        """
        Vu_A = FRC + CA * P_pl_EE - V_l_EE - V_t_EE - V_b_EE
        return Vu_A

    def larynx(self, Pao):
        """
        Larynx pressure derivative (A30)
        Cl · dPl/dt = (Pao - Pl)/Rml - (Pl - Ptr)/Rlt

        Parameters:
        - Pao: atmospheric pressure (mouth)

        Returns:
        - dPl: pressure derivative
        """
        Qin = (Pao - self.Pl) / self.Rml
        Qout = (self.Pl - self.Pt) / self.Rlt
        dPl = (Qin - Qout) / self.Cl
        return dPl

    def trachea(self):
        """
        Trachea pressure derivative (A31)
        Ct · d(Pt - Ppl)/dt = (Pl - Pt)/Rlt - (Pt - Pb)/Rtb

        Returns:
        - dPt: pressure derivative (transmural)
        """
        Qin = (self.Pl - self.Pt) / self.Rlt
        Qout = (self.Pt - self.Pb) / self.Rtb
        dPt = self.dPpl + (Qin - Qout) / self.Ct
        return dPt

    def bronchea(self):
        """
        Bronchea pressure derivative (A32)
        Cb · d(Pb - Ppl)/dt = (Pt - Pb)/Rtb - (Pb - PA)/RbA

        Returns:
        - dPb: pressure derivative (transmural)
        """
        Qin = (self.Pt - self.Pb) / self.Rtb
        Qout = (self.Pb - self.PA) / self.RbA
        dPb = self.dPpl + (Qin - Qout) / self.Cb
        return dPb

    def alveoli(self):
        """
        Alveoli pressure derivative (A33)
        CA · d(PA - Ppl)/dt = (Pb - PA)/RbA

        Returns:
        - dPA: pressure derivative (transmural)
        """
        Qin = (self.Pb - self.PA) / self.RbA
        dPA = self.dPpl + Qin / self.CA
        return dPA

    def chestWall(self):
        """
        Chest wall / pleural pressure derivative (A34)
        Ccw · d(Ppl - Pmus)/dt = (Pl - Pt)/Rlt

        Returns:
        - dPpl: pleural pressure derivative
        """
        Qin = (self.Pl - self.Pt) / self.Rlt
        dPpl = self.dPmus + Qin / self.Ccw
        return dPpl

    def flow(self, P1, P2, R):
        """
        Flow calculation (A35, A36)
        V̇ = (P1 - P2) / R

        Parameters:
        - P1: upstream pressure
        - P2: downstream pressure
        - R: resistance

        Returns:
        - Vdot: flow
        """
        Vdot = (P1 - P2) / R
        return Vdot

    def mouthFlow(self, Pao):
        """Mouth flow (A35)"""
        return self.flow(Pao, self.Pl, self.Rml)

    def alveolarFlow(self):
        """Alveolar flow (A36)"""
        return self.flow(self.Pb, self.PA, self.RbA)

    def volume(self, C, P, Vu):
        """
        Volume calculation (A37-A40)
        V = C · P + Vu

        Parameters:
        - C: compliance
        - P: transmural pressure
        - Vu: unstressed volume

        Returns:
        - V: volume
        """
        V = C * P + Vu
        return V

    def larynxVolume(self):
        """Larynx volume (A37)"""
        return self.volume(self.Cl, self.Pl, self.Vu_l)

    def tracheaVolume(self):
        """Trachea volume (A38)"""
        Ptm = self.Pt - self.Ppl
        return self.volume(self.Ct, Ptm, self.Vu_tr)

    def broncheaVolume(self):
        """Bronchea volume (A39)"""
        Ptm = self.Pb - self.Ppl
        return self.volume(self.Cb, Ptm, self.Vu_b)

    def alveolarVolume(self):
        """Alveolar volume (A40)"""
        Ptm = self.PA - self.Ppl
        return self.volume(self.CA, Ptm, self.Vu_A)

    def deadSpace(self, Vl, Vtr, Vb):
        """
        Dead space volume (A41)
        VD = Vl + Vtr + Vb

        Parameters:
        - Vl: larynx volume
        - Vtr: trachea volume
        - Vb: bronchea volume

        Returns:
        - VD: dead space volume
        """
        VD = Vl + Vtr + Vb
        return VD

    def musP(self, t, dt, Pmus_prev):
        """
        Muscle pressure pattern with derivative (Equation 4)

        Based on Albanese et al. 2016, Equation 4:
        Pmus(t) = {
            (Pmus_min/Ti·Te) · t² + (Pmus_min·T/Ti·Te) · t    for t ∈ [0, Ti]
            Pmus_min · (1 - e^(-Te/τ)) · (e^(-(t-Ti)/τ) - e^(-Te/τ)) / (1 - e^(-Te/τ))  for t ∈ [Ti, T]
        }

        Parameters:
        - t: current time in respiratory cycle
        - dt: time step
        - Pmus_prev: previous muscle pressure

        Returns:
        - Pmus: current muscle pressure
        - dPmus: muscle pressure derivative
        - tau: time constant
        """
        T = self.Ti + self.Te
        tau = self.Te / 5

        if self.b <= self.Ti:
            # Inspiratory phase - parabolic profile
            Pmus = ((-self.Pmus_min * self.b ** 2) + (self.Pmus_min * T * self.b)) / (self.Ti * self.Te)
        else:
            # Expiratory phase - exponential profile
            exp_term = np.exp(-(self.b - self.Ti) / tau) - np.exp(-self.Te / tau)
            denominator = 1 - np.exp(-self.Te / tau)
            Pmus = (self.Pmus_min * exp_term) / denominator

        # Calculate derivative
        dPmus = (Pmus - Pmus_prev) / dt

        return Pmus, dPmus, tau

    def respiration(self, t):
        """
        Respiratory timing with exercise effects (Equation 5 + Magosso & Ursino 2002)

        From Magosso & Ursino 2002, equations (7) and (8):
        Ti/Tresp = 0.4 + 0.1·I  (for I ≤ 0.2)
        Ti/Tresp = 0.6 - 0.1·I  (for 0.2 < I ≤ 1)

        Te/Tresp = 0.35 + 1.15·I  (for I ≤ 0.2)
        Te/Tresp = 0.6 - 0.1·I   (for 0.2 < I ≤ 1)

        Parameters:
        - t: current time

        Returns:
        - b: current phase time
        - Ti: inspiration time
        - Te: expiration time
        """
        # Exercise-modified timing fractions (Magosso & Ursino 2002, Eq 7-8)
        if self.exercise_intensity <= 0.2:
            Ti_fraction = 0.4 + 0.1 * self.exercise_intensity
            Te_fraction = 0.35 + 1.15 * self.exercise_intensity
        else:
            Ti_fraction = 0.6 - 0.1 * self.exercise_intensity
            Te_fraction = 0.6 - 0.1 * self.exercise_intensity

        # Base respiratory period
        T = 60.0 / self.RR

        # Exercise-modified timing
        Ti = T * Ti_fraction
        Te = T * Te_fraction

        # Current phase
        b = t % T

        return b, Ti, Te

    def phases(self):
        """
        Respiratory phase indicator

        Returns:
        - a: phase (1=inspiration, -1=expiration)
        """
        if self.b <= self.Ti:
            a = 1  # Inspiration
        else:
            a = -1  # Expiration
        return a

    def intrathoracicPressure(self, s):
        """
        Intrathoracic pressure pattern during exercise (Magosso & Ursino 2002, Eq 4-5)

        Parameters:
        - s: dimensionless respiratory cycle fraction (0-1)

        Returns:
        - Pthor: intrathoracic pressure
        """
        Tresp = self.Ti + self.Te
        Ti_frac = self.Ti / Tresp
        Te_frac = self.Te / Tresp

        # Calculate exercise-modified pressure extremes
        Pthor_min = self.Pthor_min_n - self.gthor * self.delta_VT
        Pthor_max = self.Pthor_max_n + self.gthor * self.delta_VT

        if s <= Ti_frac:
            # Inspiration - linear decrease
            Pthor = Pthor_max - (Pthor_max - Pthor_min) * (s / Ti_frac)
        elif s <= (Ti_frac + Te_frac):
            # Expiration - linear increase
            s_exp = (s - Ti_frac) / Te_frac
            Pthor = Pthor_min + (Pthor_max - Pthor_min) * s_exp
        else:
            # Respiratory pause
            Pthor = Pthor_max

        return Pthor

    def abdominalPressure(self, s):
        """
        Abdominal pressure pattern during exercise (Magosso & Ursino 2002, Eq 4-5)

        Parameters:
        - s: dimensionless respiratory cycle fraction (0-1)

        Returns:
        - Pabd: abdominal pressure
        """
        Tresp = self.Ti + self.Te
        Ti_frac = self.Ti / Tresp
        Te_frac = self.Te / Tresp
        Ti_half_frac = Ti_frac / 2

        # Calculate exercise-modified pressure extremes
        Pabd_min = self.Pabd_min_n - self.gabd * self.delta_VT
        Pabd_max = self.Pabd_max_n + self.gabd * self.delta_VT

        if s <= Ti_half_frac:
            # First half inspiration - linear decrease
            Pabd = Pabd_max - (Pabd_max - Pabd_min) * (s / Ti_half_frac)
        elif s <= Ti_frac:
            # Second half inspiration - constant minimum
            Pabd = Pabd_min
        elif s <= (Ti_frac + Te_frac):
            # Expiration - linear increase
            s_exp = (s - Ti_frac) / Te_frac
            Pabd = Pabd_min + (Pabd_max - Pabd_min) * s_exp
        else:
            # Respiratory pause
            Pabd = Pabd_max

        return Pabd

    def exerciseRespiratoryEffects(self, RR_0, Pmus_min_0, central_command_RR=0, central_command_Pmus=0):
        """
        Calculate exercise effects on respiratory parameters (Magosso & Ursino 2002)

        Exercise affects:
        1. Respiratory rate (RR)
        2. Respiratory muscle pressure amplitude (Pmus_min)

        Parameters:
        - RR_0: baseline respiratory rate (breaths/min)
        - Pmus_min_0: baseline respiratory muscle pressure amplitude (cmH2O)
        - central_command_RR: central command contribution to RR
        - central_command_Pmus: central command contribution to Pmus

        Returns:
        - RR: exercise-modified respiratory rate
        - Pmus_min: exercise-modified pressure amplitude
        """
        # Respiratory rate increase with exercise
        exercise_RR_gain = 1.0 + self.exercise_intensity * 1.5  # Up to 150% increase
        RR = RR_0 * exercise_RR_gain + central_command_RR

        # Respiratory pressure amplitude increase with exercise
        exercise_Pmus_gain = 1.0 + self.exercise_intensity * 2.0  # Up to 200% increase
        Pmus_min = Pmus_min_0 * exercise_Pmus_gain + central_command_Pmus

        return RR, Pmus_min

    def compute_derivatives(self, t, Pao, dt):
        """
        Compute all lung mechanics derivatives for one time step

        Parameters:
        - t: current time
        - Pao: atmospheric pressure (mouth pressure)
        - dt: time step

        Returns:
        - derivatives: dict with all state derivatives
        - outputs: dict with computed flows, volumes, phases
        """

        # 1. Update respiratory timing
        self.b, self.Ti, self.Te = self.respiration(t)

        # 2. Compute muscle pressure and its derivative
        Pmus, dPmus, tau = self.musP(t, dt, self.Pmus)
        self.Pmus = Pmus
        self.dPmus = dPmus
        self.tau = tau

        # 3. Compute pleural pressure derivative (A34)
        # Note: A34 gives dPpl, which we need for A31, A32, A33
        dPpl = self.chestWall()
        self.dPpl = dPpl

        # 4. Compute airway pressure derivatives (A30-A33)
        dPl = self.larynx(Pao)
        dPt = self.trachea()
        dPb = self.bronchea()
        dPA = self.alveoli()

        # 5. Compute flows (A35, A36)
        Vdot_mouth = self.mouthFlow(Pao)
        Vdot_alv = self.alveolarFlow()

        # 6. Compute volumes (A37-A40)
        Vl = self.larynxVolume()
        Vtr = self.tracheaVolume()
        Vb = self.broncheaVolume()
        VA = self.alveolarVolume()

        # 7. Compute dead space (A41)
        VD = self.deadSpace(Vl, Vtr, Vb)

        # 8. Determine respiratory phase
        phase = self.phases()

        # 9. Compute dimensionless cycle fraction for pressure patterns
        T = self.Ti + self.Te
        s = self.b / T
        Pthor = self.intrathoracicPressure(s)
        Pabd = self.abdominalPressure(s)

        # Package derivatives
        derivatives = {
            'dPl': dPl,
            'dPt': dPt,
            'dPb': dPb,
            'dPA': dPA,
            'dPpl': dPpl
        }

        # Package outputs
        outputs = {
            'Pl': self.Pl,
            'Pt': self.Pt,
            'Pb': self.Pb,
            'PA': self.PA,
            'Ppl': self.Ppl,
            'Pmus': self.Pmus,
            'dPmus': self.dPmus,
            'Vl': Vl,
            'Vtr': Vtr,
            'Vb': Vb,
            'VA': VA,
            'VD': VD,
            'Vdot_mouth': Vdot_mouth,
            'Vdot_alv': Vdot_alv,
            'phase': phase,
            'b': self.b,
            'Ti': self.Ti,
            'Te': self.Te,
            'tau': self.tau,
            's': s,
            'Pthor': Pthor,
            'Pabd': Pabd
        }

        return derivatives, outputs