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
    """

    def __init__(self, params):
        """
        Initialize systemic model with parameters

        Parameters dict should contain:
        - Systemic artery: Rsa, Lsa, Csa, Vusa
        - Peripheral: Rsp, Csp, Vusp, Rep, Cep, Vuep, Ramp, Camp, Vuamp, Rrmp, Crmp, Vurmp, Rbp, Cbp, Vubp, Rhp, Chp, Vuhp
        - Venous: Rsv, Csv, Vusv, Ramv, Camv, Vuamv, Rrmv, Crmv, Vurmv, Rbv, Cbv, Vubv, Rhv, Chv, Vuhv, Cev, Vuev
        - Active muscle veins (Magosso): P0_amv (nonlinear parameter)
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
        self.Chp = params['Chp']
        self.Vuhp = params['Vuhp']

        # Venous parameters - splanchnic
        self.Rsv = params['Rsv']
        self.Csv = params['Csv']
        self.Vusv = params['Vusv']

        # Venous parameters - active muscle (Magosso - nonlinear P-V)
        self.Ramv = params['Ramv']
        self.Camv = params['Camv']
        self.Vuamv = params['Vuamv']
        self.P0_amv = params['P0_amv']  # Nonlinear P-V parameter

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

    def splanchnicPeripheral(self):
        """Splanchnic peripheral (A6-A7)"""
        Qsp = (self.Pep - self.Psv) / self.Rsp
        Vsp = self.Csp * self.Pep + self.Vusp
        return Qsp, Vsp

    def activeMusclePeripheral(self):
        """Active muscle peripheral (A6-A7 - Magosso)"""
        Qamp = (self.Pep - self.Pamv) / self.Ramp
        Vamp = self.Camp * self.Pep + self.Vuamp
        return Qamp, Vamp

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

    def coronaryPeripheral(self):
        """Coronary peripheral (A6-A7)"""
        Qhp = (self.Pep - self.Phv) / self.Rhp
        Vhp = self.Chp * self.Pep + self.Vuhp
        return Qhp, Vhp

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

    def activeMuscleVenousNonlinear(self, Qamp, Pra, Pim):
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

        Returns:
        - dVamv: volume derivative
        - Qamv: flow to thoracic veins
        - Pamv: venous pressure
        """
        # Volume derivative (conservation)
        fin = Qamp
        fout_ra = (self.Pamv - Pra) / self.Ramv
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

        return dVamv, Qamv, self.Vamv, Pamv

    def restingMuscleVenous(self, Qrmp, Pra):
        """
        Resting muscle venous with linear P-V (standard Albanese A9, A13, A14)

        Parameters:
        - Qrmp: inflow from resting muscle peripheral
        - Pra: right atrial pressure

        Returns:
        - dPrmv: pressure derivative
        - Qrmv: flow to thoracic veins
        - Vrmv: volume
        """
        fin = Qrmp
        fout_ra = (self.Prmv - Pra) / self.Rrmv
        fout_unstressed = self.dVurmv
        fout = fout_ra + fout_unstressed
        dPrmv = (fin - fout) / self.Crmv

        Qrmv = (self.Prmv - self.Ptv) / self.Rtv
        Vrmv = self.Crmv * self.Prmv + self.Vurmv

        return dPrmv, Qrmv, Vrmv

    def splanchnicVenous(self, Qsp, Pra):
        """Splanchnic venous (A8, A13, A14)"""
        fin = Qsp
        fout_ra = (self.Psv - Pra) / self.Rsv
        fout_unstressed = self.dVusv
        fout = fout_ra + fout_unstressed
        dPsv = (fin - fout) / self.Csv

        Qsv = (self.Psv - self.Ptv) / self.Rtv
        Vsv = self.Csv * self.Psv + self.Vusv

        return dPsv, Qsv, Vsv

    def brainVenous(self, Qbp, Pra):
        """Brain venous (A10, A13, A14)"""
        fin = Qbp
        fout_ra = (self.Pbv - Pra) / self.Rbv
        dPbv = (fin - fout_ra) / self.Cbv

        Qbv = (self.Pbv - self.Ptv) / self.Rtv
        Vbv = self.Cbv * self.Pbv + self.Vubv

        return dPbv, Qbv, Vbv

    def coronaryVenous(self, Qhp, Pra):
        """Coronary venous (A11, A13, A14)"""
        fin = Qhp
        fout_ra = (self.Phv - Pra) / self.Rhv
        dPhv = (fin - fout_ra) / self.Chv

        Qhv = (self.Phv - self.Ptv) / self.Rtv
        Vhv = self.Chv * self.Phv + self.Vuhv

        return dPhv, Qhv, Vhv

    def extrasplanchnicVenous(self, Vnet):
        """Extrasplanchnic venous - volume conservation (A12, A13, A14)"""
        Vev = self.TBV - Vnet
        Pev = (Vev - self.Vuev) / self.Cev
        Qev = (Pev - self.Ptv) / self.Rtv
        return Pev, Qev, Vev

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

    def compute_derivatives(self, t, Qin, Pra):
        """
        Compute all systemic derivatives for one time step

        Parameters:
        - t: current time (for muscle pump activation)
        - Qin: inflow from left ventricle
        - Pra: right atrial pressure

        Returns:
        - derivatives: dict with all state derivatives
        - outputs: dict with computed flows and volumes
        """

        # 0. Muscle pump intramuscular pressure (Magosso)
        Pim = self.intramuscularPressure(t)

        # 1. Systemic artery
        dPsa, dQsa, Vsa = self.systemicArteryRLC(Qin)

        # 2. Peripheral flows (now 6 beds)
        Qsp, Vsp = self.splanchnicPeripheral()
        Qamp, Vamp = self.activeMusclePeripheral()
        Qrmp, Vrmp = self.restingMusclePeripheral()
        Qbp, Vbp = self.brainPeripheral()
        Qhp, Vhp = self.coronaryPeripheral()

        # 3. Extrasplanchnic peripheral + dPep
        dPep, Qep, Vep = self.extrasplanchnicPeripheral(Qsp, Qamp, Qrmp, Qbp, Qhp)

        # 4. Venous compartments (active muscle uses nonlinear P-V)
        dPsv, Qsv, Vsv = self.splanchnicVenous(Qsp, Pra)
        dVamv, Qamv, Vamv, Pamv = self.activeMuscleVenousNonlinear(Qamp, Pra, Pim)
        dPrmv, Qrmv, Vrmv = self.restingMuscleVenous(Qrmp, Pra)
        dPbv, Qbv, Vbv = self.brainVenous(Qbp, Pra)
        dPhv, Qhv, Vhv = self.coronaryVenous(Qhp, Pra)

        # 5. Calculate Vnet for extrasplanchnic venous
        Vnet = Vsa + Vsp + Vep + Vamp + Vrmp + Vbp + Vhp + Vsv + Vamv + Vrmv + Vbv + Vhv + self.Vtv

        # 6. Extrasplanchnic venous
        Pev, Qev, Vev = self.extrasplanchnicVenous(Vnet)
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
            'Qamp': Qamp, 'Vamp': Vamp,
            'Qrmp': Qrmp, 'Vrmp': Vrmp,
            'Qbp': Qbp, 'Vbp': Vbp,
            'Qhp': Qhp, 'Vhp': Vhp,
            'Qsv': Qsv, 'Vsv': Vsv,
            'Qev': Qev, 'Vev': Vev,
            'Qamv': Qamv, 'Vamv': Vamv, 'Pamv': Pamv,
            'Qrmv': Qrmv, 'Vrmv': Vrmv,
            'Qbv': Qbv, 'Vbv': Vbv,
            'Qhv': Qhv, 'Vhv': Vhv,
            'Qtv': Qtv, 'Ptv': Ptv, 'Rtv_var': Rtv_var, 'Ptm_tv': Ptm_tv,
            'Pim': Pim,
            'alpha_muscle': self.alpha_muscle
        }

        return derivatives, outputs