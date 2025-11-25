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

        # Septum parameters
        self.E_spt_es = params['E_spt_es']
        self.V_spt_d = params['V_spt_d']
        self.lambda_spt = params['lambda_spt']
        self.P_spt_0 = params['P_spt_0']
        self.V_spt_0 = params['V_spt_0']

        # Cardiac power filter (Eq 22-24, Magosso 2002)
        self.Mh_n = params['Mh_n']  # Baseline cardiac O2 consumption (mL O2/s)
        self.Wh_n = params['Wh_n']  # Baseline cardiac power (W)
        self.tau_w = params['tau_w']  # Power filter time constant (s)

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

    def lvPressure(self, LVV, E, Fout=0.0):
        """
        LV pressure from volume and activation with viscous resistance

        P_LV(t) = Pmax - R_lv * Fout
        where R_lv = kr_lv * Pmax (resistance scales with contractile pressure)

        Args:
            LVV: left ventricular volume (mL)
            E: activation (0-1)
            Fout: aortic valve outflow (mL/s)

        Returns:
            P_LV: ventricular pressure (mmHg)
            Pmax: elastic pressure without viscous term (mmHg)
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

        R_lv = self.kr_lv * Pmax
        P_LV = Pmax - R_lv * Fout

        return max(P_LV, 0.0), max(Pmax, 0.0)

    def rvPressure(self, RVV, E, Fout=0.0):
        """
        RV pressure from volume and activation with viscous resistance

        P_RV(t) = Pmax - R_rv * Fout
        where R_rv = kr_rv * Pmax (resistance scales with contractile pressure)

        Args:
            RVV: right ventricular volume (mL)
            E: activation (0-1)
            Fout: pulmonary valve outflow (mL/s)

        Returns:
            P_RV: ventricular pressure (mmHg)
            Pmax: elastic pressure without viscous term (mmHg)
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

        R_rv = self.kr_rv * Pmax
        P_RV = Pmax - R_rv * Fout

        return max(P_RV, 0.0), max(Pmax, 0.0)

    def septalVolume(self, LVP, RVP, E):
        """
        Interventricular septum volume (Albanese 2016)

        V_SPT = e(t)·V_SPT,es + [1-e(t)]·V_SPT,ed

        Args:
            LVP: left ventricular pressure (mmHg)
            RVP: right ventricular pressure (mmHg)
            E: ventricular activation (0-1)

        Returns:
            V_spt: septal volume (mL) - positive = bulges into RV
        """
        P_spt = LVP - RVP

        # End-systolic component
        V_spt_es = P_spt / self.E_spt_es + self.V_spt_d

        # End-diastolic component (piecewise for P_spt sign)
        if P_spt >= 0:
            V_spt_ed = (1.0 / self.lambda_spt) * np.log(P_spt / self.P_spt_0 + 1.0) + self.V_spt_0
        else:
            V_spt_ed = (1.0 / self.lambda_spt) * np.log(-P_spt / self.P_spt_0 + 1.0) + self.V_spt_0

        # Weighted sum
        V_spt = E * V_spt_es + (1 - E) * V_spt_ed

        return V_spt

    def trueVentricularVolumes(self, LVV, RVV, V_spt):
        """
        True ventricular volumes accounting for septal position

        V_LV = V_LVF + V_SPT
        V_RV = V_RVF - V_SPT

        Args:
            LVV: free wall LV volume (mL) - our state variable
            RVV: free wall RV volume (mL) - our state variable
            V_spt: septal volume (mL)

        Returns:
            V_LV_true: true LV volume (mL)
            V_RV_true: true RV volume (mL)
        """
        V_LV_true = LVV + V_spt
        V_RV_true = RVV - V_spt

        return V_LV_true, V_RV_true

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

    def instantaneousCardiacPower(self, LVP, RVP, dLVV, dRVV):
        """
        Instantaneous cardiac power (Magosso 2002, Eq 23).

        wh = -Plv · dVlv/dt - Prv · dVrv/dt

        Args:
            LVP: Left ventricular pressure (mmHg)
            RVP: Right ventricular pressure (mmHg)
            dLVV: LV volume derivative (mL/s)
            dRVV: RV volume derivative (mL/s)

        Returns:
            float: Instantaneous cardiac power (mmHg·mL/s)
        """
        # Negative because ejection (dV < 0) produces positive work
        wh = -LVP * dLVV - RVP * dRVV
        return max(0.0, wh)

    def cardiacPowerFilter(self, wh, Wh):
        """
        Filtered cardiac power dynamics (Magosso 2002, Eq 24).

        dWh/dt = (1/τw) · (wh - Wh)

        Args:
            wh: Instantaneous cardiac power
            Wh: Filtered cardiac power (state variable)

        Returns:
            float: dWh/dt for integration
        """
        return (wh - Wh) / self.tau_w

    def cardiacO2Consumption(self, Wh):
        """
        Cardiac O2 consumption from filtered power (Magosso 2002, Eq 22).

        Mh = (Wh / Wh,n) · Mh,n

        Args:
            Wh: Filtered cardiac power

        Returns:
            float: Cardiac O2 consumption (mL O2/s)
        """
        return (Wh / self.Wh_n) * self.Mh_n

    def compute_derivatives(self, t, LVV, RVV, LAP, RAP, Wh, Pas, Ppa, Ppv, Psv, Pev, Fav, Fpv):
        """
        Compute heart derivatives for Euler integration

        State variables (passed in):
        - LVV, RVV: ventricular volumes (mL)
        - LAP, RAP: atrial pressures (mmHg)
        - Wh: filtered cardiac power (mmHg·mL/s)

        Coupling inputs:
        - Pas: systemic arterial pressure
        - Ppa: pulmonary arterial pressure
        - Ppv: pulmonary venous pressure
        - Psv: splanchnic venous pressure
        - Pev: extrasplanchnic venous pressure
        - Fav: aortic valve flow (mL/s)
        - Fpv: pulmonary valve flow (mL/s)

        Returns:
        - derivatives: dict with dLVV, dRVV, dLAP, dRAP, dWh
        - outputs: dict with flows, pressures, volumes
        """
        # 1. Ventricular activation functions
        E_lv = self.phi(t, self.alpha_lv, self.n_lv)
        E_rv = self.phi(t, self.alpha_rv, self.n_rv)

        # 2. Ventricular pressures with viscous correction
        LVP, LVPmax = self.lvPressure(LVV, E_lv, Fav)
        RVP, RVPmax = self.rvPressure(RVV, E_rv, Fpv)
        # After computing LVP, RVP:
        V_spt = self.septalVolume(LVP, RVP, E_lv)
        V_LV_true, V_RV_true = self.trueVentricularVolumes(LVV, RVV, V_spt)

        # 3. Valve flows
        Fmv = self.valveFlow(LAP, LVP, self.Rmv)
        Fav_new = self.valveFlow(LVP, Pas, self.Rav)
        Ftv = self.valveFlow(RAP, RVP, self.Rtv)
        Fpv_new = self.valveFlow(RVP, Ppa, self.Rpv_valve)

        # 4. Atrial derivatives (compliance model)
        dLAP, Vla = self.leftAtrium(LAP, Ppv, Fmv)
        dRAP, Vra = self.rightAtrium(RAP, Psv, Pev, Ftv)

        # 5. Ventricular volume derivatives
        dLVV = Fmv - Fav_new
        dRVV = Ftv - Fpv_new

        # 6. Cardiac power (Magosso Eq 22-24)
        wh = self.instantaneousCardiacPower(LVP, RVP, dLVV, dRVV)
        dWh = self.cardiacPowerFilter(wh, Wh)
        Mh = self.cardiacO2Consumption(Wh)

        derivatives = {
            'dLVV': dLVV,
            'dRVV': dRVV,
            'dLAP': dLAP,
            'dRAP': dRAP,
            'dWh': dWh
        }

        outputs = {
            'LVP': LVP,
            'RVP': RVP,
            'LVPmax': LVPmax,
            'RVPmax': RVPmax,
            'Vla': Vla,
            'Vra': Vra,
            'Fmv': Fmv,
            'Fav': Fav_new,
            'Ftv': Ftv,
            'Fpv': Fpv_new,
            'E_lv': E_lv,
            'E_rv': E_rv,
            'wh': wh,
            'Mh': Mh,
            'V_spt': V_spt,
            'V_LV_true': V_LV_true,
            'V_RV_true': V_RV_true,
        }

        return derivatives, outputs