import numpy as np


class HeartModel:
    """
    Heart Model - Albanese 2016

    Integrates:
    - Left and right ventricles (conventional or unimodal elastance)
    - Left and right atria
    - Four valves (mitral, aortic, tricuspid, pulmonary)
    - Time-varying elastance function
    """

    def __init__(self, params):
        """
        Initialize heart model with parameters

        Parameters dict should contain:
        - Heart rate: HR
        - Timing parameters: alpha_lv, alpha_rv, alpha_la, alpha_ra, n_lv, n_rv, n_la, n_ra
        - Left ventricle: Emax_lv, E_lv, Vu_lv, kr_lv, ke_lv, P0_lv (conventional)
                         OR E_plus_lv, E_minus_lv, LVV0, P_vb_lv (unimodal)
        - Right ventricle: Emax_rv, E_rv, Vu_rv, kr_rv, ke_rv, P0_rv (conventional)
                          OR E_plus_rv, E_minus_rv, RVV0, P_vb_rv (unimodal)
        - Atria: Cla, Vu_la, Cra, Vu_ra
        - Valves: Rmv, Rav, Rtv, Rpv
        - Pulmonary veins: Rpv
        - Systemic veins: Rsv, Rev
        - Initial volumes: LVV_init, RVV_init
        - Model type: ventricle_model ('conventional' or 'unimodal')
        """
        # Store parameters
        self.params = params

        # Heart rate and timing
        self.HR = params['HR']

        # Activation function parameters - ventricles
        self.alpha_lv = params['alpha_lv']  # [alpha1, alpha2] for LV
        self.n_lv = params['n_lv']  # [n1, n2] for LV
        self.alpha_rv = params['alpha_rv']  # [alpha1, alpha2] for RV
        self.n_rv = params['n_rv']  # [n1, n2] for RV

        # Activation function parameters - atria
        self.alpha_la = params['alpha_la']  # [alpha1, alpha2] for LA
        self.n_la = params['n_la']  # [n1, n2] for LA
        self.alpha_ra = params['alpha_ra']  # [alpha1, alpha2] for RA
        self.n_ra = params['n_ra']  # [n1, n2] for RA

        # Model type
        self.ventricle_model = params.get('ventricle_model', 'conventional')

        # Left ventricle parameters
        if self.ventricle_model == 'conventional':
            self.Emax_lv = params['Emax_lv']
            self.Vu_lv = params['Vu_lv']
        else:  # unimodal
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
        else:  # unimodal
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
        self.Rmv = params['Rmv']  # Mitral
        self.Rav = params['Rav']  # Aortic
        self.Rtv = params['Rtv']  # Tricuspid
        self.Rpv_valve = params['Rpv']  # Pulmonary valve

        # Pulmonary veins resistance
        self.Rpv = params['Rpv_resistance']

        # Systemic veins resistances
        self.Rsv = params['Rsv']
        self.Rev = params['Rev']

        # Initialize state variables
        self.LVV = params.get('LVV_init', 100.0)
        self.RVV = params.get('RVV_init', 100.0)
        self.LAP = 0.0  # Left atrial pressure
        self.RAP = 0.0  # Right atrial pressure

        # Computed pressures (not state variables)
        self.LVP = 0.0
        self.RVP = 0.0

    def phi(self, t, alpha, n):
        """
        Heart activation function (normalized)

        Parameters:
        - t: time
        - alpha: [alpha1, alpha2] timing parameters
        - n: [n1, n2] shape parameters

        Returns:
        - En: normalized activation (0-1)
        """
        Tc = 60.0 / self.HR
        tm = t % Tc
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

    def leftVentricleConventional(self, E, Fin, Fout, h):
        """
        Left ventricle with conventional linear ESP

        Parameters:
        - E: normalized elastance (0-1)
        - Fin: mitral valve flow
        - Fout: aortic valve flow
        - h: time step

        Returns:
        - LVV_new: new volume
        - LVP: ventricular pressure
        - Pmax: maximum pressure
        - R: internal resistance
        """
        # Volume integration
        LVV_new = self.LVV + (Fin - Fout) * h

        # Linear ESP
        ESP = self.Emax_lv * (LVV_new - self.Vu_lv)

        # EDP
        EDP = self.P0_lv * (np.exp(self.ke_lv * LVV_new) - 1)

        # Pressure
        Pmax = E * ESP + (1 - E) * EDP
        R = self.kr_lv * Pmax
        LVP = Pmax - R * Fout

        return LVV_new, LVP, Pmax, R

    def leftVentricleUnimodal(self, E, Fin, Fout, h):
        """
        Left ventricle with unimodal ESP

        Parameters:
        - E: normalized elastance (0-1)
        - Fin: mitral valve flow
        - Fout: aortic valve flow
        - h: time step

        Returns:
        - LVV_new: new volume
        - LVP: ventricular pressure
        - Pmax: maximum pressure
        - R: internal resistance
        """
        # Volume integration
        LVV_new = self.LVV + (Fin - Fout) * h

        # Calculate breakpoint volume
        breakpoint = (self.E_plus_lv * self.LVV0 + self.P_vb_lv) / (self.E_plus_lv - self.E_minus_lv)

        # Piecewise ESP
        if LVV_new < self.LVV0:
            ESP = 0
        elif LVV_new <= breakpoint:
            ESP = self.E_plus_lv * (LVV_new - self.LVV0)
        else:
            ESP = self.E_minus_lv * LVV_new + self.P_vb_lv

        # EDP
        EDP = self.P0_lv * (np.exp(self.ke_lv * LVV_new) - 1)

        # Pressure
        Pmax = E * ESP + (1 - E) * EDP
        R = self.kr_lv * Pmax
        LVP = Pmax - R * Fout

        return LVV_new, LVP, Pmax, R

    def rightVentricleConventional(self, E, Fin, Fout, h):
        """
        Right ventricle with conventional linear ESP

        Parameters:
        - E: normalized elastance (0-1)
        - Fin: tricuspid valve flow
        - Fout: pulmonary valve flow
        - h: time step

        Returns:
        - RVV_new: new volume
        - RVP: ventricular pressure
        - Pmax: maximum pressure
        - R: internal resistance
        """
        # Volume integration
        RVV_new = self.RVV + (Fin - Fout) * h

        # Linear ESP
        ESP = self.Emax_rv * (RVV_new - self.Vu_rv)

        # EDP
        EDP = self.P0_rv * (np.exp(self.ke_rv * RVV_new) - 1)

        # Pressure
        Pmax = E * ESP + (1 - E) * EDP
        R = self.kr_rv * Pmax
        RVP = Pmax - R * Fout

        return RVV_new, RVP, Pmax, R

    def rightVentricleUnimodal(self, E, Fin, Fout, h):
        """
        Right ventricle with unimodal ESP

        Parameters:
        - E: normalized elastance (0-1)
        - Fin: tricuspid valve flow
        - Fout: pulmonary valve flow
        - h: time step

        Returns:
        - RVV_new: new volume
        - RVP: ventricular pressure
        - Pmax: maximum pressure
        - R: internal resistance
        """
        # Volume integration
        RVV_new = self.RVV + (Fin - Fout) * h

        # Calculate breakpoint volume
        breakpoint = (self.E_plus_rv * self.RVV0 + self.P_vb_rv) / (self.E_plus_rv - self.E_minus_rv)

        # Piecewise ESP
        if RVV_new < self.RVV0:
            ESP = 0
        elif RVV_new <= breakpoint:
            ESP = self.E_plus_rv * (RVV_new - self.RVV0)
        else:
            ESP = self.E_minus_rv * RVV_new + self.P_vb_rv

        # EDP
        EDP = self.P0_rv * (np.exp(self.ke_rv * RVV_new) - 1)

        # Pressure
        Pmax = E * ESP + (1 - E) * EDP
        R = self.kr_rv * Pmax
        RVP = Pmax - R * Fout

        return RVV_new, RVP, Pmax, R

    def leftAtrium(self, Ppv, Fmv):
        """
        Left atrium pressure derivative

        Parameters:
        - Ppv: pulmonary venous pressure
        - Fmv: mitral valve flow (outflow)

        Returns:
        - dLAP: pressure derivative
        - Vla: volume
        """
        Fin = (Ppv - self.LAP) / self.Rpv
        dLAP = (Fin - Fmv) / self.Cla
        Vla = self.Cla * self.LAP + self.Vu_la
        return dLAP, Vla

    def rightAtrium(self, Psv, Pev, Ftv):
        """
        Right atrium pressure derivative

        Parameters:
        - Psv: splanchnic venous pressure
        - Pev: extrasplanchnic venous pressure
        - Ftv: tricuspid valve flow (outflow)

        Returns:
        - dRAP: pressure derivative
        - Vra: volume
        """
        Fin = (Psv - self.RAP) / self.Rsv + (Pev - self.RAP) / self.Rev
        dRAP = (Fin - Ftv) / self.Cra
        Vra = self.Cra * self.RAP + self.Vu_ra
        return dRAP, Vra

    def valveFlow(self, Pin, Pout, R):
        """
        Unidirectional valve flow

        Parameters:
        - Pin: upstream pressure
        - Pout: downstream pressure
        - R: valve resistance

        Returns:
        - F: flow (0 if closed)
        """
        if Pin <= Pout:
            F = 0.0
        else:
            F = (Pin - Pout) / R
        return F

    def mitralValve(self):
        """Mitral valve flow (LA -> LV)"""
        return self.valveFlow(self.LAP, self.LVP, self.Rmv)

    def aorticValve(self, Pas):
        """Aortic valve flow (LV -> Aorta)"""
        return self.valveFlow(self.LVP, Pas, self.Rav)

    def tricuspidValve(self):
        """Tricuspid valve flow (RA -> RV)"""
        return self.valveFlow(self.RAP, self.RVP, self.Rtv)

    def pulmonaryValve(self, Ppa):
        """Pulmonary valve flow (RV -> Pulmonary artery)"""
        return self.valveFlow(self.RVP, Ppa, self.Rpv_valve)

    def compute_derivatives(self, t, Pas, Ppa, Ppv, Psv, Pev, h):
        """
        Compute all heart derivatives for one time step

        Parameters:
        - t: current time
        - Pas: systemic arterial pressure (from systemic model)
        - Ppa: pulmonary arterial pressure (from pulmonary model)
        - Ppv: pulmonary venous pressure (from pulmonary model)
        - Psv: systemic venous pressure (from systemic model)
        - Pev: extrasplanchnic venous pressure (from systemic model)
        - h: time step

        Returns:
        - derivatives: dict with all state derivatives
        - outputs: dict with computed flows, pressures, volumes
        """

        # 1. Compute activation functions
        E_lv = self.phi(t, self.alpha_lv, self.n_lv)
        E_rv = self.phi(t, self.alpha_rv, self.n_rv)
        E_la = self.phi(t, self.alpha_la, self.n_la)
        E_ra = self.phi(t, self.alpha_ra, self.n_ra)

        # 2. Compute ventricular pressures (need these for valve flows)
        if self.ventricle_model == 'conventional':
            # Initial estimate with zero flows
            _, self.LVP, _, _ = self.leftVentricleConventional(E_lv, 0, 0, h)
            _, self.RVP, _, _ = self.rightVentricleConventional(E_rv, 0, 0, h)
        else:
            _, self.LVP, _, _ = self.leftVentricleUnimodal(E_lv, 0, 0, h)
            _, self.RVP, _, _ = self.rightVentricleUnimodal(E_rv, 0, 0, h)

        # 3. Compute valve flows
        Fmv = self.mitralValve()
        Fav = self.aorticValve(Pas)
        Ftv = self.tricuspidValve()
        Fpv = self.pulmonaryValve(Ppa)

        # 4. Update ventricles with actual flows
        if self.ventricle_model == 'conventional':
            LVV_new, LVP, Pmax_lv, R_lv = self.leftVentricleConventional(E_lv, Fmv, Fav, h)
            RVV_new, RVP, Pmax_rv, R_rv = self.rightVentricleConventional(E_rv, Ftv, Fpv, h)
        else:
            LVV_new, LVP, Pmax_lv, R_lv = self.leftVentricleUnimodal(E_lv, Fmv, Fav, h)
            RVV_new, RVP, Pmax_rv, R_rv = self.rightVentricleUnimodal(E_rv, Ftv, Fpv, h)

        # 5. Update pressures
        self.LVP = LVP
        self.RVP = RVP

        # 6. Compute atrial derivatives
        dLAP, Vla = self.leftAtrium(Ppv, Fmv)
        dRAP, Vra = self.rightAtrium(Psv, Pev, Ftv)

        # 7. Compute volume derivatives
        dLVV = (Fmv - Fav)
        dRVV = (Ftv - Fpv)

        # Update state variables
        self.LVV = LVV_new
        self.RVV = RVV_new

        # Package derivatives
        derivatives = {
            'dLVV': dLVV,
            'dRVV': dRVV,
            'dLAP': dLAP,
            'dRAP': dRAP
        }

        # Package outputs
        outputs = {
            'LVV': self.LVV,
            'RVV': self.RVV,
            'LVP': self.LVP,
            'RVP': self.RVP,
            'LAP': self.LAP,
            'RAP': self.RAP,
            'Vla': Vla,
            'Vra': Vra,
            'Fmv': Fmv,
            'Fav': Fav,
            'Ftv': Ftv,
            'Fpv': Fpv,
            'E_lv': E_lv,
            'E_rv': E_rv,
            'E_la': E_la,
            'E_ra': E_ra,
            'Pmax_lv': Pmax_lv,
            'Pmax_rv': Pmax_rv,
            'R_lv': R_lv,
            'R_rv': R_rv
        }

        return derivatives, outputs