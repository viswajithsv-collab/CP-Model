import numpy as np


class HeartModel:
    """
    Heart Model - Albanese 2016 (RK45 Compatible)

    State Variables (4):
    - LVV: left ventricular volume (mL)
    - RVV: right ventricular volume (mL)
    - LAP: left atrial pressure (mmHg)
    - RAP: right atrial pressure (mmHg)
    """

    def __init__(self, params):
        # Store parameters
        self.params = params

        # Heart rate and timing
        self.HR = params['HR']

        # Activation function parameters - ventricles
        self.alpha_lv = params['alpha_lv']
        self.n_lv = params['n_lv']
        self.alpha_rv = params['alpha_rv']
        self.n_rv = params['n_rv']

        # Activation function parameters - atria
        self.alpha_la = params['alpha_la']
        self.n_la = params['n_la']
        self.alpha_ra = params['alpha_ra']
        self.n_ra = params['n_ra']

        # Model type
        self.ventricle_model = params.get('ventricle_model', 'conventional')

        # Left ventricle parameters
        if self.ventricle_model == 'conventional':
            self.Emax_lv = params['Emax_lv']
            self.Vu_lv = params['Vu_lv']
        else:
            self.E_plus_lv = params['E_plus_lv']
            self.E_minus_lv = params['E_minus_lv']
            self.LVV0 = params['LVV0']
            self.P_vb_lv = params['P_vb_lv']

        self.kr_lv = params['kr_lv']
        self.ke_lv = params['ke_lv']
        self.P0_lv = params['P0_lv']

        # Right ventricle parameters
        if self.ventricle_model == 'conventional':
            self.Emax_rv = params['Emax_rv']
            self.Vu_rv = params['Vu_rv']
        else:
            self.E_plus_rv = params['E_plus_rv']
            self.E_minus_rv = params['E_minus_rv']
            self.RVV0 = params['RVV0']
            self.P_vb_rv = params['P_vb_rv']

        self.kr_rv = params['kr_rv']
        self.ke_rv = params['ke_rv']
        self.P0_rv = params['P0_rv']

        # Atrial parameters
        self.Cla = params['Cla']
        self.Vu_la = params['Vu_la']
        self.Cra = params['Cra']
        self.Vu_ra = params['Vu_ra']

        # Valve resistances
        self.Rmv = params['Rmv']
        self.Rav = params['Rav']
        self.Rtv = params['Rtv']
        self.Rpv_valve = params['Rpv']

        # Pulmonary veins resistance
        self.Rpv = params['Rpv_resistance']

        # Systemic veins resistances
        self.Rsv = params['Rsv']
        self.Rev = params['Rev']

    def phi(self, t, alpha, n):
        """
        Heart activation function (normalized 0-1)
        """
        Tc = 60.0 / self.HR
        tm = t % Tc
        x = tm / Tc

        if alpha[0] <= 0 or alpha[1] <= 0:
            return 0.0

        a1 = x / alpha[0]
        a2 = x / alpha[1]

        m = a1 ** n[0]
        o = a2 ** n[1]

        p = m / (1 + m)
        q = 1 / (1 + o)

        z = p * q

        # Normalize by max value
        x_max = np.sqrt(alpha[0] * alpha[1])
        a1_max = x_max / alpha[0]
        a2_max = x_max / alpha[1]
        m_max = a1_max ** n[0]
        o_max = a2_max ** n[1]
        z_max = (m_max / (1 + m_max)) * (1 / (1 + o_max))

        if z_max > 0:
            En = z / z_max
        else:
            En = 0.0

        return min(max(En, 0.0), 1.0)

    def lvPressure(self, LVV, E):
        """
        LV pressure from volume and activation (algebraic, no h)
        """
        if self.ventricle_model == 'conventional':
            ESP = self.Emax_lv * (LVV - self.Vu_lv)
        else:
            breakpoint = (self.E_plus_lv * self.LVV0 + self.P_vb_lv) / (self.E_plus_lv - self.E_minus_lv)
            if LVV < self.LVV0:
                ESP = 0
            elif LVV <= breakpoint:
                ESP = self.E_plus_lv * (LVV - self.LVV0)
            else:
                ESP = self.E_minus_lv * LVV + self.P_vb_lv

        EDP = self.P0_lv * (np.exp(self.ke_lv * LVV) - 1)
        Pmax = E * ESP + (1 - E) * EDP
        return max(Pmax, 0.0)

    def rvPressure(self, RVV, E):
        """
        RV pressure from volume and activation (algebraic, no h)
        """
        if self.ventricle_model == 'conventional':
            ESP = self.Emax_rv * (RVV - self.Vu_rv)
        else:
            breakpoint = (self.E_plus_rv * self.RVV0 + self.P_vb_rv) / (self.E_plus_rv - self.E_minus_rv)
            if RVV < self.RVV0:
                ESP = 0
            elif RVV <= breakpoint:
                ESP = self.E_plus_rv * (RVV - self.RVV0)
            else:
                ESP = self.E_minus_rv * RVV + self.P_vb_rv

        EDP = self.P0_rv * (np.exp(self.ke_rv * RVV) - 1)
        Pmax = E * ESP + (1 - E) * EDP
        return max(Pmax, 0.0)

    def leftAtrium(self, LAP, Ppv, Fmv):
        """
        Left atrium pressure derivative

        Parameters:
        - LAP: left atrial pressure (state variable, passed in)
        - Ppv: pulmonary venous pressure
        - Fmv: mitral valve flow (outflow)

        Returns:
        - dLAP: pressure derivative
        - Vla: volume
        """
        Fin = (Ppv - LAP) / self.Rpv
        dLAP = (Fin - Fmv) / self.Cla
        Vla = self.Cla * LAP + self.Vu_la
        return dLAP, Vla

    def rightAtrium(self, RAP, Psv, Pev, Ftv):
        """
        Right atrium pressure derivative

        Parameters:
        - RAP: right atrial pressure (state variable, passed in)
        - Psv: splanchnic venous pressure
        - Pev: extrasplanchnic venous pressure
        - Ftv: tricuspid valve flow (outflow)

        Returns:
        - dRAP: pressure derivative
        - Vra: volume
        """
        Fin = (Psv - RAP) / self.Rsv + (Pev - RAP) / self.Rev
        dRAP = (Fin - Ftv) / self.Cra
        Vra = self.Cra * RAP + self.Vu_ra
        return dRAP, Vra

    def valveFlow(self, Pin, Pout, R):
        """Unidirectional valve flow"""
        if Pin > Pout:
            return (Pin - Pout) / R
        return 0.0

    def compute_derivatives(self, t, LVV, RVV, LAP, RAP, Pas, Ppa, Ppv, Psv, Pev):
        """
        Compute heart derivatives for RK45

        State variables (passed in):
        - LVV, RVV: ventricular volumes (mL)
        - LAP, RAP: atrial pressures (mmHg)

        Coupling inputs:
        - Pas: systemic arterial pressure
        - Ppa: pulmonary arterial pressure
        - Ppv: pulmonary venous pressure
        - Psv: splanchnic venous pressure
        - Pev: extrasplanchnic venous pressure

        Returns:
        - derivatives: dict with dLVV, dRVV, dLAP, dRAP
        - outputs: dict with flows, pressures, volumes
        """
        # 1. Activation functions
        E_lv = self.phi(t, self.alpha_lv, self.n_lv)
        E_rv = self.phi(t, self.alpha_rv, self.n_rv)
        E_la = self.phi(t, self.alpha_la, self.n_la)
        E_ra = self.phi(t, self.alpha_ra, self.n_ra)

        # 2. Ventricular pressures (algebraic)
        LVP = self.lvPressure(LVV, E_lv)
        RVP = self.rvPressure(RVV, E_rv)

        # 3. Valve flows
        Fmv = self.valveFlow(LAP, LVP, self.Rmv)
        Fav = self.valveFlow(LVP, Pas, self.Rav)
        Ftv = self.valveFlow(RAP, RVP, self.Rtv)
        Fpv = self.valveFlow(RVP, Ppa, self.Rpv_valve)

        # 4. Atrial derivatives (using original methods)
        dLAP, Vla = self.leftAtrium(LAP, Ppv, Fmv)
        dRAP, Vra = self.rightAtrium(RAP, Psv, Pev, Ftv)

        # 5. DERIVATIVES
        dLVV = Fmv - Fav
        dRVV = Ftv - Fpv
        # dLAP, dRAP already computed above

        derivatives = {
            'dLVV': dLVV,
            'dRVV': dRVV,
            'dLAP': dLAP,
            'dRAP': dRAP
        }

        outputs = {
            'LVV': LVV,
            'RVV': RVV,
            'LVP': LVP,
            'RVP': RVP,
            'LAP': LAP,
            'RAP': RAP,
            'Vla': Vla,
            'Vra': Vra,
            'Fmv': Fmv,
            'Fav': Fav,
            'Ftv': Ftv,
            'Fpv': Fpv,
            'E_lv': E_lv,
            'E_rv': E_rv,
            'E_la': E_la,
            'E_ra': E_ra
        }

        return derivatives, outputs