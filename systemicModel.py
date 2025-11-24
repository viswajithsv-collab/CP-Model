import numpy as np


class SystemicModel:
    """
    Systemic circulation model - Albanese 2016 + Magosso 2002 extensions

    Integrates:
    - Systemic arteries (A1-A3)
    - 6 peripheral beds: splanchnic, extrasplanchnic, active muscle, resting muscle, brain, coronary
    - 6 venous compartments (with nonlinear P-V for active muscle veins)
    - Thoracic veins with nonlinear P-V
    - Muscle pump mechanics (Magosso Eq 1-3)
    - Starling resistor for venous outflow (Eq 11)
    - Variable active muscle venous resistance (Eq 12)
    - O2 autoregulation on peripheral resistances (Eq 16, 17)
    """

    def __init__(self, params):
        """
        Initialize systemic model with parameters

        Parameters dict should contain:
        - Systemic artery: Rsa, Lsa, Csa, Vusa
        - Peripheral: Rsp, Csp, Vusp, Rep, Cep, Vuep, Ramp, Camp, Vuamp, Rrmp, Crmp, Vurmp, Rbp, Cbp, Vubp, Rhp, Chp, Vuhp
        - Venous: Rsv, Csv, Vusv, Ramv, Camv, Vuamv, Rrmv, Crmv, Vurmv, Rbv, Cbv, Vubv, Rhv, Chv, Vuhv, Cev, Vuev
        - Active muscle veins (Magosso): P0_amv (nonlinear parameter), kr_am (Eq 12)
        - Muscle pump: A_pump, Tc (contraction cycle), Tim (contraction duration), alpha_muscle
        - Thoracic veins: D1, K1, Vutv, D2, K2, Vtv_min, K_xp, K_xv, KR, Vtv_max, Rtv_0
        - Resistances to thoracic veins: Rtv
        - Total blood volume: TBV
        """
        # Store parameters
        self.params = params

        # Systemic artery parameters
        self.Rsa = params['Rsa']
        self.Lsa = params['Lsa']
        self.Csa = params['Csa']
        self.Vusa = params['Vusa']

        # Peripheral parameters - splanchnic
        self.Rsp = params['Rsp']
        self.Csp = params['Csp']
        self.Vusp = params['Vusp']

        # Peripheral parameters - extrasplanchnic
        self.Rep = params['Rep']
        self.Cep = params['Cep']
        self.Vuep = params['Vuep']

        # Peripheral parameters - active muscle (Magosso)
        self.Ramp = params['Ramp']
        self.Ramp_n = params.get('Ramp_n', params['Ramp'])  # Baseline for autoregulation (Eq 16)
        self.Camp = params['Camp']
        self.Vuamp = params['Vuamp']

        # Peripheral parameters - resting muscle (Magosso)
        self.Rrmp = params['Rrmp']
        self.Crmp = params['Crmp']
        self.Vurmp = params['Vurmp']

        # Peripheral parameters - brain
        self.Rbp = params['Rbp']
        self.Cbp = params['Cbp']
        self.Vubp = params['Vubp']

        # Peripheral parameters - coronary
        self.Rhp = params['Rhp']
        self.Rhp_n = params.get('Rhp_n', params['Rhp'])  # Baseline for autoregulation (Eq 17)
        self.Chp = params['Chp']
        self.Vuhp = params['Vuhp']

        # Venous parameters - splanchnic
        self.Rsv = params['Rsv']
        self.Csv = params['Csv']
        self.Vusv = params['Vusv']

        # Venous parameters - active muscle (Magosso - nonlinear P-V)
        self.Ramv = params['Ramv']
        self.Ramv_n = params.get('Ramv_n', params['Ramv'])  # Baseline resistance
        self.Camv = params['Camv']
        self.Vuamv = params['Vuamv']
        self.P0_amv = params['P0_amv']  # Nonlinear P-V parameter (Eq 1)
        self.kr_am = params.get('kr_am', 24.17)  # Variable resistance parameter (Eq 12)

        # Venous parameters - resting muscle (linear P-V)
        self.Rrmv = params['Rrmv']
        self.Crmv = params['Crmv']
        self.Vurmv = params['Vurmv']

        # Venous parameters - brain
        self.Rbv = params['Rbv']
        self.Cbv = params['Cbv']
        self.Vubv = params['Vubv']

        # Venous parameters - coronary
        self.Rhv = params['Rhv']
        self.Chv = params['Chv']
        self.Vuhv = params['Vuhv']

        # Venous parameters - extrasplanchnic
        self.Cev = params['Cev']
        self.Vuev = params['Vuev']

        # Muscle pump parameters (Magosso Eq 2-3)
        self.A_pump = params.get('A_pump', 0.0)  # Peak intramuscular pressure
        self.Tc = params.get('Tc', 1.0)  # Muscle contraction cycle duration
        self.Tim = params.get('Tim', 0.4)  # Muscle contraction duration
        self.alpha_muscle = 0.0  # Dimensionless cycle fraction

        # Thoracic veins parameters
        self.D1 = params['D1']
        self.K1 = params['K1']
        self.Vutv = params['Vutv']
        self.D2 = params['D2']
        self.K2 = params['K2']
        self.Vtv_min = params['Vtv_min']
        self.K_xp = params['K_xp']
        self.K_xv = params['K_xv']
        self.KR = params['KR']
        self.Vtv_max = params['Vtv_max']
        self.Rtv_0 = params['Rtv_0']
        self.Rtv = params['Rtv']

        # Total blood volume
        self.TBV = params['TBV']

        # Initialize state variables
        self.Psa = 0.0
        self.Qsa = 0.0
        self.Pep = 0.0

        # Venous pressures
        self.Psv = 0.0  # Splanchnic
        self.Pamv = 0.0  # Active muscle
        self.Prmv = 0.0  # Resting muscle
        self.Pbv = 0.0  # Brain
        self.Phv = 0.0  # Coronary
        self.Pev = 0.0  # Extrasplanchnic

        # Active muscle venous volume (needed for nonlinear P-V)
        self.Vamv = params.get('Vamv_init', 100.0)

        # Thoracic veins
        self.Vtv = params.get('Vtv_init', 200.0)
        self.Ptv = 0.0

        # Pleural pressure (external input)
        self.Ppl = 0.0

        # Unstressed volume changes
        self.dVusv = 0.0
        self.dVuamv = 0.0
        self.dVurmv = 0.0

    # =========================================================================
    # STARLING RESISTOR (Eq 11)
    # =========================================================================

    def starlingResistor(self, Rjv_n, Pjv, Ptv, Pj=0.0):
        """
        Starling resistor for venous outflow (Eq 11)

        Rjv = {
            Rjv,n                               if Ptv > Pj
            Rjv,n · (Ptv - Pv) / (Pjv - Pj)     if Ptv < Pj
        }

        When thoracic vein pressure drops below external pressure (Pj),
        the effective resistance increases due to venous collapse.

        Parameters:
        - Rjv_n: nominal venous resistance (mmHg·s/mL)
        - Pjv: venous compartment pressure (mmHg)
        - Ptv: thoracic vein pressure (mmHg)
        - Pj: external pressure (mmHg)
              Pj = Pabd for splanchnic (j=s)
              Pj = 0 for all others (j=b, h, e, rm)

        Returns:
        - Rjv: effective venous resistance (mmHg·s/mL)

        Note: This does NOT apply to active muscle (j=am) in resting conditions.
              Active muscle uses Eq 12 instead during exercise.
        """
        if Ptv > Pj:
            # Normal flow - nominal resistance
            Rjv = Rjv_n
        else:
            # Venous collapse - increased resistance
            # Avoid division by zero
            denom = Pjv - Pj
            if abs(denom) < 1e-6:
                Rjv = Rjv_n * 10.0  # High resistance when collapsed
            else:
                Rjv = Rjv_n * (Ptv - Pj) / denom
                # Ensure resistance doesn't go negative or too low
                Rjv = max(Rjv, Rjv_n * 0.1)

        return Rjv

    # =========================================================================
    # ACTIVE MUSCLE VENOUS RESISTANCE (Eq 12)
    # =========================================================================

    def activeMuscleVenousResistance(self, Vamv):
        """
        Variable active muscle venous resistance during exercise (Eq 12)

        Ramv = kr,am / Vamv

        Resistance is inversely proportional to blood volume contained
        in the active muscle venous compartment.

        Parameters:
        - Vamv: active muscle venous volume (mL)

        Returns:
        - Ramv: active muscle venous resistance (mmHg·s/mL)
        """
        # Prevent division by zero
        Vamv_safe = max(Vamv, 1.0)

        Ramv = self.kr_am / Vamv_safe

        return Ramv

    # =========================================================================
    # SYSTEMIC ARTERIES
    # =========================================================================

    def systemicArteryRLC(self, Qin):
        """Systemic arteries with inertance (A1-A3)"""
        dQsa = (self.Psa - self.Pep - self.Rsa * self.Qsa) / self.Lsa
        dPsa = (Qin - self.Qsa) / self.Csa
        Vsa = self.Csa * self.Psa + self.Vusa
        return dPsa, dQsa, Vsa

    def systemicArteryRC(self, Qin):
        """Systemic arteries without inertance (A1, A3)"""
        Qsa = (self.Psa - self.Pep) / self.Rsa
        dPsa = (Qin - Qsa) / self.Csa
        Vsa = self.Csa * self.Psa + self.Vusa
        return dPsa, Qsa, Vsa

    # =========================================================================
    # PERIPHERAL COMPARTMENTS
    # =========================================================================

    def splanchnicPeripheral(self):
        """Splanchnic peripheral (A6-A7)"""
        Qsp = (self.Pep - self.Psv) / self.Rsp
        Vsp = self.Csp * self.Pep + self.Vusp
        return Qsp, Vsp

    def activeMusclePeripheral(self, x_am_O2=0.0, x_met=0.0):
        """
        Active muscle peripheral with O2 autoregulation (A6-A7, Eq 16)

        Ramp = Ramp,n / (1 + x_am,O2 + x_met)

        Parameters:
        - x_am_O2: O2 autoregulation state variable (from ControlSystemModel)
        - x_met: metabolic vasodilator state variable (from ControlSystemModel)

        Returns:
        - Qamp: flow through active muscle peripheral (mL/s)
        - Vamp: volume in active muscle peripheral (mL)
        - Ramp_eff: effective resistance (mmHg·s/mL)
        """
        # Effective resistance with autoregulation (Eq 16)
        Ramp_eff = self.Ramp_n / (1.0 + x_am_O2 + x_met)

        Qamp = (self.Pep - self.Pamv) / Ramp_eff
        Vamp = self.Camp * self.Pep + self.Vuamp

        return Qamp, Vamp, Ramp_eff

    def restingMusclePeripheral(self):
        """Resting muscle peripheral (A6-A7 - Magosso)"""
        Qrmp = (self.Pep - self.Prmv) / self.Rrmp
        Vrmp = self.Crmp * self.Pep + self.Vurmp
        return Qrmp, Vrmp

    def brainPeripheral(self):
        """Brain peripheral (A6-A7)"""
        Qbp = (self.Pep - self.Pbv) / self.Rbp
        Vbp = self.Cbp * self.Pep + self.Vubp
        return Qbp, Vbp

    def coronaryPeripheral(self, x_h_O2=0.0):
        """
        Coronary peripheral with O2 autoregulation (A6-A7, Eq 17)

        Rhp = Rhp,n / (1 + x_h,O2)

        Parameters:
        - x_h_O2: coronary O2 autoregulation state variable (from ControlSystemModel)

        Returns:
        - Qhp: flow through coronary peripheral (mL/s)
        - Vhp: volume in coronary peripheral (mL)
        - Rhp_eff: effective resistance (mmHg·s/mL)
        """
        # Effective resistance with autoregulation (Eq 17)
        Rhp_eff = self.Rhp_n / (1.0 + x_h_O2)

        Qhp = (self.Pep - self.Phv) / Rhp_eff
        Vhp = self.Chp * self.Pep + self.Vuhp

        return Qhp, Vhp, Rhp_eff

    def extrasplanchnicPeripheral(self, Qsp, Qamp, Qrmp, Qbp, Qhp):
        """
        Extrasplanchnic peripheral - MASTER (A4-A7)
        Now includes both active and resting muscle flows
        """
        Qep = (self.Pep - self.Pev) / self.Rep

        # Total compliance (now includes both active and resting muscle)
        Ctot = self.Csp + self.Cep + self.Camp + self.Crmp + self.Cbp + self.Chp

        # Total outflow (now includes both active and resting muscle)
        Qout_total = Qsp + Qep + Qamp + Qrmp + Qbp + Qhp

        dPep = (self.Qsa - Qout_total) / Ctot
        Vep = self.Cep * self.Pep + self.Vuep

        return dPep, Qep, Vep

    # =========================================================================
    # MUSCLE PUMP (Eq 2-3)
    # =========================================================================

    def musclePumpActivation(self, t):
        """
        Muscle pump activation function (Magosso Eq 3)

        ψ(t) = {
            sin(π · Tim/Tc · α)     if 0 ≤ α ≤ Tc/Tim
            0                        if Tc/Tim ≤ α ≤ 1
        }

        where α = (t mod Tc) / Tc is dimensionless cycle fraction
        """
        # Dimensionless cycle fraction
        self.alpha_muscle = (t % self.Tc) / self.Tc

        # Activation function
        if self.alpha_muscle <= (self.Tim / self.Tc):
            psi = np.sin(np.pi * (self.Tim / self.Tc) * self.alpha_muscle)
        else:
            psi = 0.0

        return psi

    def intramuscularPressure(self, t):
        """
        Intramuscular pressure (Magosso Eq 2)
        Pim = A · ψ(t)
        """
        psi = self.musclePumpActivation(t)
        Pim = self.A_pump * psi
        return Pim

    # =========================================================================
    # VENOUS COMPARTMENTS
    # =========================================================================

    def activeMuscleVenousNonlinear(self, Qamp, Pra, Pim, use_variable_resistance=False):
        """
        Active muscle venous with nonlinear P-V (Magosso Eq 1)

        Pamv - Pim = {
            (1/Camv) · (Vamv - Vuamv)                if Vamv > Vuamv
            P0 · [1 - (Vamv/Vuamv)^(-3/2)]          if Vamv < Vuamv
        }

        Parameters:
        - Qamp: inflow from active muscle peripheral
        - Pra: right atrial pressure
        - Pim: intramuscular pressure (muscle pump)
        - use_variable_resistance: if True, use Eq 12 for Ramv

        Returns:
        - dVamv: volume derivative
        - Qamv: flow to thoracic veins
        - Vamv: current volume
        - Pamv: venous pressure
        - Ramv_eff: effective resistance used
        """
        # Determine resistance (Eq 12 or nominal)
        if use_variable_resistance:
            Ramv_eff = self.activeMuscleVenousResistance(self.Vamv)
        else:
            Ramv_eff = self.Ramv_n

        # Volume derivative (conservation)
        fin = Qamp
        fout_ra = (self.Pamv - Pra) / Ramv_eff
        fout_unstressed = self.dVuamv
        fout = fout_ra + fout_unstressed

        # Nonlinear P-V relationship (Magosso Eq 1)
        if self.Vamv > self.Vuamv:
            # Linear regime (veins open)
            Pamv = Pim + (1.0 / self.Camv) * (self.Vamv - self.Vuamv)
        else:
            # Nonlinear regime (veins collapsed)
            Pamv = Pim + self.P0_amv * (1.0 - (self.Vamv / self.Vuamv) ** (-3.0 / 2.0))

        # Update pressure state
        self.Pamv = Pamv

        # Volume derivative
        dVamv = fin - fout

        # Flow to thoracic veins
        Qamv = (self.Pamv - self.Ptv) / self.Rtv

        return dVamv, Qamv, self.Vamv, Pamv, Ramv_eff

    def restingMuscleVenous(self, Qrmp, Pra, Pabd=0.0, use_starling=False):
        """
        Resting muscle venous with linear P-V (standard Albanese A9, A13, A14)
        Optional Starling resistor (Eq 11)

        Parameters:
        - Qrmp: inflow from resting muscle peripheral
        - Pra: right atrial pressure
        - Pabd: abdominal pressure (for Starling resistor)
        - use_starling: if True, apply Starling resistor (Eq 11)

        Returns:
        - dPrmv: pressure derivative
        - Qrmv: flow to thoracic veins
        - Vrmv: volume
        - Rrmv_eff: effective resistance used
        """
        # Determine resistance (Eq 11 or nominal)
        if use_starling:
            Rrmv_eff = self.starlingResistor(self.Rrmv, self.Prmv, self.Ptv, Pj=0.0)
        else:
            Rrmv_eff = self.Rrmv

        fin = Qrmp
        fout_ra = (self.Prmv - Pra) / Rrmv_eff
        fout_unstressed = self.dVurmv
        fout = fout_ra + fout_unstressed
        dPrmv = (fin - fout) / self.Crmv

        Qrmv = (self.Prmv - self.Ptv) / self.Rtv
        Vrmv = self.Crmv * self.Prmv + self.Vurmv

        return dPrmv, Qrmv, Vrmv, Rrmv_eff

    def splanchnicVenous(self, Qsp, Pra, Pabd=0.0, use_starling=False):
        """
        Splanchnic venous (A8, A13, A14)
        Optional Starling resistor (Eq 11) with abdominal pressure

        Parameters:
        - Qsp: inflow from splanchnic peripheral
        - Pra: right atrial pressure
        - Pabd: abdominal pressure (for Starling resistor, Pj = Pabd)
        - use_starling: if True, apply Starling resistor (Eq 11)

        Returns:
        - dPsv: pressure derivative
        - Qsv: flow to thoracic veins
        - Vsv: volume
        - Rsv_eff: effective resistance used
        """
        # Determine resistance (Eq 11 or nominal)
        if use_starling:
            Rsv_eff = self.starlingResistor(self.Rsv, self.Psv, self.Ptv, Pj=Pabd)
        else:
            Rsv_eff = self.Rsv

        fin = Qsp
        fout_ra = (self.Psv - Pra) / Rsv_eff
        fout_unstressed = self.dVusv
        fout = fout_ra + fout_unstressed
        dPsv = (fin - fout) / self.Csv

        Qsv = (self.Psv - self.Ptv) / self.Rtv
        Vsv = self.Csv * self.Psv + self.Vusv

        return dPsv, Qsv, Vsv, Rsv_eff

    def brainVenous(self, Qbp, Pra, use_starling=False):
        """
        Brain venous (A10, A13, A14)
        Optional Starling resistor (Eq 11)

        Parameters:
        - Qbp: inflow from brain peripheral
        - Pra: right atrial pressure
        - use_starling: if True, apply Starling resistor (Eq 11)

        Returns:
        - dPbv: pressure derivative
        - Qbv: flow to thoracic veins
        - Vbv: volume
        - Rbv_eff: effective resistance used
        """
        # Determine resistance (Eq 11 or nominal)
        if use_starling:
            Rbv_eff = self.starlingResistor(self.Rbv, self.Pbv, self.Ptv, Pj=0.0)
        else:
            Rbv_eff = self.Rbv

        fin = Qbp
        fout_ra = (self.Pbv - Pra) / Rbv_eff
        dPbv = (fin - fout_ra) / self.Cbv

        Qbv = (self.Pbv - self.Ptv) / self.Rtv
        Vbv = self.Cbv * self.Pbv + self.Vubv

        return dPbv, Qbv, Vbv, Rbv_eff

    def coronaryVenous(self, Qhp, Pra, use_starling=False):
        """
        Coronary venous (A11, A13, A14)
        Optional Starling resistor (Eq 11)

        Parameters:
        - Qhp: inflow from coronary peripheral
        - Pra: right atrial pressure
        - use_starling: if True, apply Starling resistor (Eq 11)

        Returns:
        - dPhv: pressure derivative
        - Qhv: flow to thoracic veins
        - Vhv: volume
        - Rhv_eff: effective resistance used
        """
        # Determine resistance (Eq 11 or nominal)
        if use_starling:
            Rhv_eff = self.starlingResistor(self.Rhv, self.Phv, self.Ptv, Pj=0.0)
        else:
            Rhv_eff = self.Rhv

        fin = Qhp
        fout_ra = (self.Phv - Pra) / Rhv_eff
        dPhv = (fin - fout_ra) / self.Chv

        Qhv = (self.Phv - self.Ptv) / self.Rtv
        Vhv = self.Chv * self.Phv + self.Vuhv

        return dPhv, Qhv, Vhv, Rhv_eff

    def extrasplanchnicVenous(self, Vnet, use_starling=False):
        """
        Extrasplanchnic venous - volume conservation (A12, A13, A14)
        Optional Starling resistor (Eq 11)

        Parameters:
        - Vnet: sum of all other compartment volumes
        - use_starling: if True, apply Starling resistor (Eq 11)

        Returns:
        - Pev: extrasplanchnic venous pressure
        - Qev: flow to thoracic veins
        - Vev: volume
        - Rev_eff: effective resistance used
        """
        Vev = self.TBV - Vnet
        Pev = (Vev - self.Vuev) / self.Cev

        # Determine resistance (Eq 11 or nominal)
        if use_starling:
            Rev_eff = self.starlingResistor(self.Rev, Pev, self.Ptv, Pj=0.0)
        else:
            Rev_eff = self.Rev

        Qev = (Pev - self.Ptv) / self.Rtv

        return Pev, Qev, Vev, Rev_eff

    # =========================================================================
    # THORACIC VEINS
    # =========================================================================

    def thoracicVeins(self, Qsv, Qev, Qamv, Qrmv, Qbv, Qhv, Pra):
        """
        Thoracic veins with nonlinear P-V (A15-A17, Eq 2-3)
        Now includes both active and resting muscle venous flows
        """
        Qin_total = Qsv + Qev + Qamv + Qrmv + Qbv + Qhv

        Ptm_tv = self._nonlinearPV(self.Vtv)
        Ptv = self.Ppl + Ptm_tv
        Rtv_var = self._variableResistance(self.Vtv)
        Qtv = (Ptv - Pra) / Rtv_var
        dVtv = Qin_total - Qtv

        return dVtv, Ptv, Qtv, Rtv_var, Ptm_tv

    def _nonlinearPV(self, Vtv):
        """Thoracic veins nonlinear P-V (Equation 2)"""
        psi = self.K_xp / (np.exp(Vtv / self.K_xv) - 1)

        if Vtv >= self.Vutv:
            Ptm_tv = self.D1 + self.K1 * (Vtv - self.Vutv) - psi
        else:
            Ptm_tv = self.D2 + self.K2 * np.exp(Vtv / self.Vtv_min) - psi

        return Ptm_tv

    def _variableResistance(self, Vtv):
        """Thoracic veins variable resistance (Equation 3)"""
        Rtv_var = self.KR * (self.Vtv_max / Vtv) ** 2 + self.Rtv_0
        return Rtv_var

    # =========================================================================
    # MASTER COMPUTE DERIVATIVES
    # =========================================================================

    def compute_derivatives(self, t, Qin, Pra, x_am_O2=0.0, x_met=0.0, x_h_O2=0.0,
                            Pabd=0.0, use_starling=False, use_variable_Ramv=False):
        """
        Compute all systemic derivatives for one time step

        Parameters:
        - t: current time (for muscle pump activation)
        - Qin: inflow from left ventricle
        - Pra: right atrial pressure
        - x_am_O2: active muscle O2 autoregulation state (Eq 16)
        - x_met: metabolic vasodilator state (Eq 16)
        - x_h_O2: coronary O2 autoregulation state (Eq 17)
        - Pabd: abdominal pressure (for Starling resistor)
        - use_starling: if True, apply Starling resistor (Eq 11)
        - use_variable_Ramv: if True, use variable Ramv (Eq 12)

        Returns:
        - derivatives: dict with all state derivatives
        - outputs: dict with computed flows and volumes
        """

        # 0. Muscle pump intramuscular pressure (Magosso)
        Pim = self.intramuscularPressure(t)

        # 1. Systemic artery
        dPsa, dQsa, Vsa = self.systemicArteryRLC(Qin)

        # 2. Peripheral flows (now 6 beds, with autoregulation)
        Qsp, Vsp = self.splanchnicPeripheral()
        Qamp, Vamp, Ramp_eff = self.activeMusclePeripheral(x_am_O2, x_met)
        Qrmp, Vrmp = self.restingMusclePeripheral()
        Qbp, Vbp = self.brainPeripheral()
        Qhp, Vhp, Rhp_eff = self.coronaryPeripheral(x_h_O2)

        # 3. Extrasplanchnic peripheral + dPep
        dPep, Qep, Vep = self.extrasplanchnicPeripheral(Qsp, Qamp, Qrmp, Qbp, Qhp)

        # 4. Venous compartments (with optional Starling and variable resistance)
        dPsv, Qsv, Vsv, Rsv_eff = self.splanchnicVenous(Qsp, Pra, Pabd, use_starling)
        dVamv, Qamv, Vamv, Pamv, Ramv_eff = self.activeMuscleVenousNonlinear(
            Qamp, Pra, Pim, use_variable_Ramv
        )
        dPrmv, Qrmv, Vrmv, Rrmv_eff = self.restingMuscleVenous(Qrmp, Pra, Pabd, use_starling)
        dPbv, Qbv, Vbv, Rbv_eff = self.brainVenous(Qbp, Pra, use_starling)
        dPhv, Qhv, Vhv, Rhv_eff = self.coronaryVenous(Qhp, Pra, use_starling)

        # 5. Calculate Vnet for extrasplanchnic venous
        Vnet = Vsa + Vsp + Vep + Vamp + Vrmp + Vbp + Vhp + Vsv + Vamv + Vrmv + Vbv + Vhv + self.Vtv

        # 6. Extrasplanchnic venous
        Pev, Qev, Vev, Rev_eff = self.extrasplanchnicVenous(Vnet, use_starling)
        self.Pev = Pev

        # 7. Thoracic veins
        dVtv, Ptv, Qtv, Rtv_var, Ptm_tv = self.thoracicVeins(Qsv, Qev, Qamv, Qrmv, Qbv, Qhv, Pra)
        self.Ptv = Ptv

        # Update active muscle venous volume state
        self.Vamv = Vamv

        # Package derivatives
        derivatives = {
            'dPsa': dPsa,
            'dQsa': dQsa,
            'dPep': dPep,
            'dPsv': dPsv,
            'dVamv': dVamv,  # Active muscle: volume derivative (nonlinear P-V)
            'dPrmv': dPrmv,  # Resting muscle: pressure derivative (linear P-V)
            'dPbv': dPbv,
            'dPhv': dPhv,
            'dVtv': dVtv
        }

        # Package outputs
        outputs = {
            'Vsa': Vsa,
            'Qsp': Qsp, 'Vsp': Vsp,
            'Qep': Qep, 'Vep': Vep,
            'Qamp': Qamp, 'Vamp': Vamp, 'Ramp_eff': Ramp_eff,
            'Qrmp': Qrmp, 'Vrmp': Vrmp,
            'Qbp': Qbp, 'Vbp': Vbp,
            'Qhp': Qhp, 'Vhp': Vhp, 'Rhp_eff': Rhp_eff,
            'Qsv': Qsv, 'Vsv': Vsv, 'Rsv_eff': Rsv_eff,
            'Qev': Qev, 'Vev': Vev, 'Rev_eff': Rev_eff,
            'Qamv': Qamv, 'Vamv': Vamv, 'Pamv': Pamv, 'Ramv_eff': Ramv_eff,
            'Qrmv': Qrmv, 'Vrmv': Vrmv, 'Rrmv_eff': Rrmv_eff,
            'Qbv': Qbv, 'Vbv': Vbv, 'Rbv_eff': Rbv_eff,
            'Qhv': Qhv, 'Vhv': Vhv, 'Rhv_eff': Rhv_eff,
            'Qtv': Qtv, 'Ptv': Ptv, 'Rtv_var': Rtv_var, 'Ptm_tv': Ptm_tv,
            'Pim': Pim,
            'alpha_muscle': self.alpha_muscle
        }

        return derivatives, outputs
