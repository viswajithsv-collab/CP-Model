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

    States: Pl, Pt, Pb, PA, Ppl (5)
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

        # Alveolar unstressed volume
        self.Vu_A = params['Vu_A']

        # Respiratory timing
        self.RR = params['RR']  # Respiratory rate (breaths/min)
        self.IE = params['IE']  # I/E ratio

        # Muscle pressure
        self.Pmus_min = params['Pmus_min']

        # Exercise parameters
        self.exercise_intensity = params['exercise_intensity']
        self.gthor = params['gthor']
        self.gabd = params['gabd']
        self.delta_VT = params['delta_VT']

        # Baseline pressure extremes
        self.Pthor_min_n = params['Pthor_min_n']
        self.Pthor_max_n = params['Pthor_max_n']
        self.Pabd_min_n = params['Pabd_min_n']
        self.Pabd_max_n = params['Pabd_max_n']

    def calculateVuA(self, FRC, CA, P_pl_EE, V_l_EE, V_t_EE, V_b_EE):
        """
        Calculate alveolar unstressed volume from FRC (Equation 6)
        Vu,A = FRC + CA * Ppl,EE - Vl,EE - Vt,EE - Vb,EE

        Utility method - can be used to compute Vu_A before passing to params
        """
        Vu_A = FRC + CA * P_pl_EE - V_l_EE - V_t_EE - V_b_EE
        return Vu_A

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

    def musclePressure(self, b, Ti, Te):
        """
        Muscle pressure pattern with analytical derivative (Equation 4)

        Based on Albanese et al. 2016, Equation 4:
        Pmus(t) = {
            (-Pmus_min/Ti·Te) · b² + (Pmus_min·T/Ti·Te) · b    for b ∈ [0, Ti]
            Pmus_min · (e^(-(b-Ti)/τ) - e^(-Te/τ)) / (1 - e^(-Te/τ))  for b ∈ [Ti, T]
        }

        Parameters:
        - b: current phase time within respiratory cycle
        - Ti: inspiration time
        - Te: expiration time

        Returns:
        - Pmus: current muscle pressure
        - dPmus: muscle pressure derivative (analytical)
        - tau: time constant
        """
        T = Ti + Te
        tau = Te / 5.0

        if b <= Ti:
            # Inspiratory phase - parabolic profile
            denom = Ti * Te
            Pmus = ((-self.Pmus_min * b ** 2) + (self.Pmus_min * T * b)) / denom
            # Analytical derivative: d/db[(-Pmus_min·b² + Pmus_min·T·b)/(Ti·Te)]
            dPmus = ((-2.0 * self.Pmus_min * b) + (self.Pmus_min * T)) / denom
        else:
            # Expiratory phase - exponential profile
            b_exp = b - Ti
            exp_b = np.exp(-b_exp / tau)
            exp_Te = np.exp(-Te / tau)
            denom = 1.0 - exp_Te

            Pmus = (self.Pmus_min * (exp_b - exp_Te)) / denom
            # Analytical derivative: d/db[Pmus_min·(e^(-(b-Ti)/τ) - e^(-Te/τ))/(1 - e^(-Te/τ))]
            dPmus = (self.Pmus_min * (-1.0 / tau) * exp_b) / denom

        return Pmus, dPmus, tau

    def intrathoracicPressure(self, s, Ti, Te):
        """
        Intrathoracic pressure pattern during exercise (Magosso & Ursino 2002, Eq 4-5)

        Parameters:
        - s: dimensionless respiratory cycle fraction (0-1)
        - Ti: inspiration time
        - Te: expiration time

        Returns:
        - Pthor: intrathoracic pressure
        """
        Tresp = Ti + Te
        Ti_frac = Ti / Tresp
        Te_frac = Te / Tresp

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

    def abdominalPressure(self, s, Ti, Te):
        """
        Abdominal pressure pattern during exercise (Magosso & Ursino 2002, Eq 4-5)

        Parameters:
        - s: dimensionless respiratory cycle fraction (0-1)
        - Ti: inspiration time
        - Te: expiration time

        Returns:
        - Pabd: abdominal pressure
        """
        Tresp = Ti + Te
        Ti_frac = Ti / Tresp
        Te_frac = Te / Tresp
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

        Parameters:
        - RR_0: baseline respiratory rate (breaths/min)
        - Pmus_min_0: baseline respiratory muscle pressure amplitude (cmH2O)
        - central_command_RR: central command contribution to RR
        - central_command_Pmus: central command contribution to Pmus

        Returns:
        - RR: exercise-modified respiratory rate
        - Pmus_min: exercise-modified pressure amplitude
        """
        exercise_RR_gain = 1.0 + self.exercise_intensity * 1.5
        RR = RR_0 * exercise_RR_gain + central_command_RR

        exercise_Pmus_gain = 1.0 + self.exercise_intensity * 2.0
        Pmus_min = Pmus_min_0 * exercise_Pmus_gain + central_command_Pmus

        return RR, Pmus_min

    # =========================================================================
    # MASTER COMPUTE DERIVATIVES
    # =========================================================================

    def compute_derivatives(self, t, Pl, Pt, Pb, PA, Ppl, Pao=0.0):
        """
        Compute all lung mechanics derivatives for Euler integration

        Albanese 2016 Equations A30-A41

        State variables (passed in):
        - Pl: larynx pressure (mmHg)
        - Pt: trachea pressure (mmHg)
        - Pb: bronchea pressure (mmHg)
        - PA: alveolar pressure (mmHg)
        - Ppl: pleural pressure (mmHg)

        Coupling inputs:
        - Pao: atmospheric/mouth pressure (mmHg), default 0.0

        Returns:
        - derivatives: dict with dPl, dPt, dPb, dPA, dPpl
        - outputs: dict with flows, volumes, Pmus, phase, timing
        """

        # 1. Respiratory timing
        b, Ti, Te = self.respiration(t)
        T = Ti + Te

        # 2. Muscle pressure and analytical derivative (Eq 4)
        Pmus, dPmus, tau = self.musclePressure(b, Ti, Te)

        # 3. Flows
        Qml = (Pao - Pl) / self.Rml  # Mouth to larynx
        Qlt = (Pl - Pt) / self.Rlt  # Larynx to trachea
        Qtb = (Pt - Pb) / self.Rtb  # Trachea to bronchea
        QbA = (Pb - PA) / self.RbA  # Bronchea to alveoli

        # 4. Pressure derivatives (A30-A34)
        # A34: Chest wall - Ccw · d(Ppl - Pmus)/dt = Qlt
        dPpl = dPmus + Qlt / self.Ccw

        # A30: Larynx - Cl · dPl/dt = Qml - Qlt
        dPl = (Qml - Qlt) / self.Cl

        # A31: Trachea - Ct · d(Pt - Ppl)/dt = Qlt - Qtb
        dPt = dPpl + (Qlt - Qtb) / self.Ct

        # A32: Bronchea - Cb · d(Pb - Ppl)/dt = Qtb - QbA
        dPb = dPpl + (Qtb - QbA) / self.Cb

        # A33: Alveoli - CA · d(PA - Ppl)/dt = QbA
        dPA = dPpl + QbA / self.CA

        # 5. Volumes (A37-A40)
        Vl = self.Cl * Pl + self.Vu_l  # A37: Larynx
        Vtr = self.Ct * (Pt - Ppl) + self.Vu_tr  # A38: Trachea (transmural)
        Vb = self.Cb * (Pb - Ppl) + self.Vu_b  # A39: Bronchea (transmural)
        VA = self.CA * (PA - Ppl) + self.Vu_A  # A40: Alveoli (transmural)

        # 6. Dead space (A41)
        VD = Vl + Vtr + Vb

        # 7. Respiratory phase
        phase = 1 if b <= Ti else -1  # 1=inspiration, -1=expiration

        # 8. Pressure patterns
        s = b / T
        Pthor = self.intrathoracicPressure(s, Ti, Te)
        Pabd = self.abdominalPressure(s, Ti, Te)

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
            'Pmus': Pmus,
            'dPmus': dPmus,
            'Vl': Vl,
            'Vtr': Vtr,
            'Vb': Vb,
            'VA': VA,
            'VD': VD,
            'Vdot_mouth': Qml,
            'Vdot_alv': QbA,
            'phase': phase,
            'b': b,
            'Ti': Ti,
            'Te': Te,
            'tau': tau,
            's': s,
            'Pthor': Pthor,
            'Pabd': Pabd
        }

        return derivatives, outputs