import numpy as np
from parameters import ALBANESE_PARAMS


class SystemicModel:
    """
    Systemic circulation model for Albanese 2016
    
    Integrates:
    - Systemic arteries (A1-A3)
    - 5 peripheral beds (splanchnic, extrasplanchnic, muscle, brain, coronary)
    - 5 venous compartments
    - Thoracic veins with nonlinear P-V
    """
    
    def __init__(self, params=None):
        """
        Initialize systemic model with parameters
        
        Parameters dict should contain:
        - Systemic artery: Rsa, Lsa, Csa, Vusa
        - Peripheral: Rsp, Csp, Vusp, Rep, Cep, Vuep, Rmp, Cmp, Vump, Rbp, Cbp, Vubp, Rhp, Chp, Vuhp
        - Venous: Rsv, Csv, Vusv, Rmv, Cmv, Vumv, Rbv, Cbv, Vubv, Rhv, Chv, Vuhv, Cev, Vuev
        - Thoracic veins: D1, K1, Vutv, D2, K2, Vtv_min, K_xp, K_xv, KR, Vtv_max, Rtv_0
        - Resistances to thoracic veins: Rtv (same for all beds)
        - Total blood volume: TBV
        
        If params is None, uses ALBANESE_PARAMS from parameters.py
        """
        # Use default parameters if none provided
        if params is None:
            params = ALBANESE_PARAMS
        
        # Store parameters
        self.params = params
        
        # Systemic artery parameters
        self.Rsa = params['Rsa']
        self.Lsa = params['Lsa']
        self.Csa = params['Csa']
        self.Vusa = params['Vusa']
        
        # Peripheral parameters
        self.Rsp = params['Rsp']
        self.Csp = params['Csp']
        self.Vusp = params['Vusp']
        
        self.Rep = params['Rep']
        self.Cep = params['Cep']
        self.Vuep = params['Vuep']
        
        self.Rmp = params['Rmp']
        self.Cmp = params['Cmp']
        self.Vump = params['Vump']
        
        self.Rbp = params['Rbp']
        self.Cbp = params['Cbp']
        self.Vubp = params['Vubp']
        
        self.Rhp = params['Rhp']
        self.Chp = params['Chp']
        self.Vuhp = params['Vuhp']
        
        # Venous parameters
        self.Rsv = params['Rsv']
        self.Csv = params['Csv']
        self.Vusv = params['Vusv']
        
        self.Rmv = params['Rmv']
        self.Cmv = params['Cmv']
        self.Vumv = params['Vumv']
        
        self.Rbv = params['Rbv']
        self.Cbv = params['Cbv']
        self.Vubv = params['Vubv']
        
        self.Rhv = params['Rhv']
        self.Chv = params['Chv']
        self.Vuhv = params['Vuhv']
        
        self.Cev = params['Cev']
        self.Vuev = params['Vuev']
        
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
        self.Rtv = params['Rtv']  # Resistance to thoracic veins (same for all beds)
        
        # Total blood volume
        self.TBV = params['TBV']
        
        # Initialize state variables
        self.Psa = 0.0  # Systemic arterial pressure
        self.Qsa = 0.0  # Systemic arterial flow
        self.Pep = 0.0  # Equivalent peripheral pressure
        
        # Venous pressures
        self.Psv = 0.0  # Splanchnic venous
        self.Pmv = 0.0  # Muscle venous
        self.Pbv = 0.0  # Brain venous
        self.Phv = 0.0  # Coronary venous
        self.Pev = 0.0  # Extrasplanchnic venous
        
        # Thoracic veins
        self.Vtv = params.get('Vtv_init', 200.0)  # Initial thoracic veins volume
        self.Ptv = 0.0  # Thoracic venous pressure
        
        # Pleural pressure (external input)
        self.Ppl = 0.0  # Will be set by respiratory model or kept at 0
        
        # Unstressed volume changes (for venous compartments)
        self.dVusv = 0.0
        self.dVumv = 0.0
    
    
    def systemicArteryRLC(self, Qin):
        """
        Systemic arteries with inertance (RLC model)
        Equations A1-A3
        
        Parameters:
        - Qin: inflow from left ventricle
        
        Returns:
        - dPsa: pressure derivative
        - dQsa: flow derivative
        - Vsa: volume
        """
        # A2: Flow derivative
        dQsa = (self.Psa - self.Pep - self.Rsa * self.Qsa) / self.Lsa
        
        # A1: Pressure derivative
        dPsa = (Qin - self.Qsa) / self.Csa
        
        # A3: Volume
        Vsa = self.Csa * self.Psa + self.Vusa
        
        return dPsa, dQsa, Vsa
    
    
    def systemicArteryRC(self, Qin):
        """
        Systemic arteries without inertance (RC model)
        Simplified version of A1
        
        Parameters:
        - Qin: inflow from left ventricle
        
        Returns:
        - dPsa: pressure derivative
        - Qsa: algebraic flow
        - Vsa: volume
        """
        # Algebraic flow
        Qsa = (self.Psa - self.Pep) / self.Rsa
        
        # A1: Pressure derivative
        dPsa = (Qin - Qsa) / self.Csa
        
        # A3: Volume
        Vsa = self.Csa * self.Psa + self.Vusa
        
        return dPsa, Qsa, Vsa
    
    
    def splanchnicPeripheral(self):
        """
        Splanchnic peripheral compartment
        Equations A6-A7
        
        Returns:
        - Qsp: flow to venous side
        - Vsp: volume
        """
        Qsp = (self.Pep - self.Psv) / self.Rsp
        Vsp = self.Csp * self.Pep + self.Vusp
        return Qsp, Vsp
    
    
    def musclePeripheral(self):
        """
        Muscle peripheral compartment
        Equations A6-A7
        
        Returns:
        - Qmp: flow to venous side
        - Vmp: volume
        """
        Qmp = (self.Pep - self.Pmv) / self.Rmp
        Vmp = self.Cmp * self.Pep + self.Vump
        return Qmp, Vmp
    
    
    def brainPeripheral(self):
        """
        Brain peripheral compartment
        Equations A6-A7
        
        Returns:
        - Qbp: flow to venous side
        - Vbp: volume
        """
        Qbp = (self.Pep - self.Pbv) / self.Rbp
        Vbp = self.Cbp * self.Pep + self.Vubp
        return Qbp, Vbp
    
    
    def coronaryPeripheral(self):
        """
        Coronary peripheral compartment
        Equations A6-A7
        
        Returns:
        - Qhp: flow to venous side
        - Vhp: volume
        """
        Qhp = (self.Pep - self.Phv) / self.Rhp
        Vhp = self.Chp * self.Pep + self.Vuhp
        return Qhp, Vhp
    
    
    def extrasplanchnicPeripheral(self, Qsp, Qmp, Qbp, Qhp):
        """
        Extrasplanchnic peripheral - MASTER compartment
        Calculates dPep using all peripheral flows
        Equations A4-A7
        
        Parameters:
        - Qsp, Qmp, Qbp, Qhp: flows from other peripheral beds
        
        Returns:
        - dPep: equivalent peripheral pressure derivative
        - Qep: extrasplanchnic flow
        - Vep: extrasplanchnic volume
        """
        # A6: Extrasplanchnic flow
        Qep = (self.Pep - self.Pev) / self.Rep
        
        # A4: Total peripheral compliance
        Ctot = self.Csp + self.Cep + self.Cmp + self.Cbp + self.Chp
        
        # A4: Total outflow
        Qout_total = Qsp + Qep + Qmp + Qbp + Qhp
        
        # A4: Equivalent peripheral pressure derivative
        dPep = (self.Qsa - Qout_total) / Ctot
        
        # A7: Extrasplanchnic volume
        Vep = self.Cep * self.Pep + self.Vuep
        
        return dPep, Qep, Vep
    
    
    def splanchnicVenous(self, Qsp, Pra):
        """
        Splanchnic venous compartment
        Equations A8, A13, A14
        
        Parameters:
        - Qsp: inflow from peripheral
        - Pra: right atrial pressure
        
        Returns:
        - dPsv: pressure derivative
        - Qsv: flow to thoracic veins
        - Vsv: volume
        """
        # A8: Pressure derivative
        fin = Qsp
        fout_ra = (self.Psv - Pra) / self.Rsv
        fout_unstressed = self.dVusv
        fout = fout_ra + fout_unstressed
        dPsv = (fin - fout) / self.Csv
        
        # A13: Flow to thoracic veins
        Qsv = (self.Psv - self.Ptv) / self.Rtv
        
        # A14: Volume
        Vsv = self.Csv * self.Psv + self.Vusv
        
        return dPsv, Qsv, Vsv
    
    
    def muscleVenous(self, Qmp, Pra):
        """
        Muscle venous compartment
        Equations A9, A13, A14
        
        Parameters:
        - Qmp: inflow from peripheral
        - Pra: right atrial pressure
        
        Returns:
        - dPmv: pressure derivative
        - Qmv: flow to thoracic veins
        - Vmv: volume
        """
        # A9: Pressure derivative
        fin = Qmp
        fout_ra = (self.Pmv - Pra) / self.Rmv
        fout_unstressed = self.dVumv
        fout = fout_ra + fout_unstressed
        dPmv = (fin - fout) / self.Cmv
        
        # A13: Flow to thoracic veins
        Qmv = (self.Pmv - self.Ptv) / self.Rtv
        
        # A14: Volume
        Vmv = self.Cmv * self.Pmv + self.Vumv
        
        return dPmv, Qmv, Vmv
    
    
    def brainVenous(self, Qbp, Pra):
        """
        Brain venous compartment
        Equations A10, A13, A14
        
        Parameters:
        - Qbp: inflow from peripheral
        - Pra: right atrial pressure
        
        Returns:
        - dPbv: pressure derivative
        - Qbv: flow to thoracic veins
        - Vbv: volume
        """
        # A10: Pressure derivative
        fin = Qbp
        fout_ra = (self.Pbv - Pra) / self.Rbv
        dPbv = (fin - fout_ra) / self.Cbv
        
        # A13: Flow to thoracic veins
        Qbv = (self.Pbv - self.Ptv) / self.Rtv
        
        # A14: Volume
        Vbv = self.Cbv * self.Pbv + self.Vubv
        
        return dPbv, Qbv, Vbv
    
    
    def coronaryVenous(self, Qhp, Pra):
        """
        Coronary venous compartment
        Equations A11, A13, A14
        
        Parameters:
        - Qhp: inflow from peripheral
        - Pra: right atrial pressure
        
        Returns:
        - dPhv: pressure derivative
        - Qhv: flow to thoracic veins
        - Vhv: volume
        """
        # A11: Pressure derivative
        fin = Qhp
        fout_ra = (self.Phv - Pra) / self.Rhv
        dPhv = (fin - fout_ra) / self.Chv
        
        # A13: Flow to thoracic veins
        Qhv = (self.Phv - self.Ptv) / self.Rtv
        
        # A14: Volume
        Vhv = self.Chv * self.Phv + self.Vuhv
        
        return dPhv, Qhv, Vhv
    
    
    def extrasplanchnicVenous(self, Vnet):
        """
        Extrasplanchnic venous - volume conservation
        Equations A12, A13, A14
        
        Parameters:
        - Vnet: sum of all OTHER compartment volumes
        
        Returns:
        - Pev: pressure (algebraic)
        - Qev: flow to thoracic veins
        - Vev: volume
        """
        # A12: Volume conservation
        Vev = self.TBV - Vnet
        
        # Pressure from volume
        Pev = (Vev - self.Vuev) / self.Cev
        
        # A13: Flow to thoracic veins
        Qev = (Pev - self.Ptv) / self.Rtv
        
        return Pev, Qev, Vev
    
    
    def thoracicVeins(self, Qsv, Qev, Qmv, Qbv, Qhv, Pra):
        """
        Thoracic veins with nonlinear P-V and variable resistance
        Equations A15-A17, Eq 2, Eq 3
        
        Parameters:
        - Qsv, Qev, Qmv, Qbv, Qhv: inflows from venous beds
        - Pra: right atrial pressure
        
        Returns:
        - dVtv: volume derivative
        - Ptv: pressure
        - Qtv: outflow to RA
        - Rtv_var: variable resistance
        - Ptm_tv: transmural pressure
        """
        # Total inflow (A15)
        Qin_total = Qsv + Qev + Qmv + Qbv + Qhv
        
        # Nonlinear P-V relationship (Eq 2)
        Ptm_tv = self._nonlinearPV(self.Vtv)
        
        # A17: Total pressure
        Ptv = self.Ppl + Ptm_tv
        
        # Variable resistance (Eq 3)
        Rtv_var = self._variableResistance(self.Vtv)
        
        # A16: Outflow to RA
        Qtv = (Ptv - Pra) / Rtv_var
        
        # A15: Volume derivative
        dVtv = Qin_total - Qtv
        
        return dVtv, Ptv, Qtv, Rtv_var, Ptm_tv
    
    
    def _nonlinearPV(self, Vtv):
        """Helper: Nonlinear P-V relationship (Equation 2)"""
        psi = self.K_xp / (np.exp(Vtv / self.K_xv) - 1)
        
        if Vtv >= self.Vutv:
            Ptm_tv = self.D1 + self.K1 * (Vtv - self.Vutv) - psi
        else:
            Ptm_tv = self.D2 + self.K2 * np.exp(Vtv / self.Vtv_min) - psi
        
        return Ptm_tv
    
    
    def _variableResistance(self, Vtv):
        """Helper: Variable resistance (Equation 3)"""
        Rtv_var = self.KR * (self.Vtv_max / Vtv) ** 2 + self.Rtv_0
        return Rtv_var
    
    
    def compute_derivatives(self, Qin, Pra):
        """
        Compute all systemic derivatives for one time step
        
        Parameters:
        - Qin: inflow from left ventricle (aortic valve)
        - Pra: right atrial pressure (from heart model)
        
        Returns:
        - derivatives: dict with all state derivatives
        - outputs: dict with computed flows and volumes
        """
        # 1. Systemic artery (choose RLC or RC)
        dPsa, dQsa, Vsa = self.systemicArteryRLC(Qin)
        
        # 2. Peripheral flows (algebraic)
        Qsp, Vsp = self.splanchnicPeripheral()
        Qmp, Vmp = self.musclePeripheral()
        Qbp, Vbp = self.brainPeripheral()
        Qhp, Vhp = self.coronaryPeripheral()
        
        # 3. Extrasplanchnic peripheral + dPep calculation
        dPep, Qep, Vep = self.extrasplanchnicPeripheral(Qsp, Qmp, Qbp, Qhp)
        
        # 4. Venous compartments
        dPsv, Qsv, Vsv = self.splanchnicVenous(Qsp, Pra)
        dPmv, Qmv, Vmv = self.muscleVenous(Qmp, Pra)
        dPbv, Qbv, Vbv = self.brainVenous(Qbp, Pra)
        dPhv, Qhv, Vhv = self.coronaryVenous(Qhp, Pra)
        
        # 5. Calculate Vnet for extrasplanchnic venous
        Vnet = Vsa + Vsp + Vep + Vmp + Vbp + Vhp + Vsv + Vmv + Vbv + Vhv + self.Vtv
        
        # 6. Extrasplanchnic venous (volume conservation)
        Pev, Qev, Vev = self.extrasplanchnicVenous(Vnet)
        
        # Update Pev state
        self.Pev = Pev
        
        # 7. Thoracic veins
        dVtv, Ptv, Qtv, Rtv_var, Ptm_tv = self.thoracicVeins(Qsv, Qev, Qmv, Qbv, Qhv, Pra)
        
        # Update Ptv state
        self.Ptv = Ptv
        
        # Package derivatives
        derivatives = {
            'dPsa': dPsa,
            'dQsa': dQsa,
            'dPep': dPep,
            'dPsv': dPsv,
            'dPmv': dPmv,
            'dPbv': dPbv,
            'dPhv': dPhv,
            'dVtv': dVtv
        }
        
        # Package outputs
        outputs = {
            'Vsa': Vsa,
            'Qsp': Qsp, 'Vsp': Vsp,
            'Qep': Qep, 'Vep': Vep,
            'Qmp': Qmp, 'Vmp': Vmp,
            'Qbp': Qbp, 'Vbp': Vbp,
            'Qhp': Qhp, 'Vhp': Vhp,
            'Qsv': Qsv, 'Vsv': Vsv,
            'Qev': Qev, 'Vev': Vev,
            'Qmv': Qmv, 'Vmv': Vmv,
            'Qbv': Qbv, 'Vbv': Vbv,
            'Qhv': Qhv, 'Vhv': Vhv,
            'Qtv': Qtv, 'Ptv': Ptv, 'Rtv_var': Rtv_var, 'Ptm_tv': Ptm_tv
        }
        
        return derivatives, outputs
