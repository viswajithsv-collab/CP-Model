import numpy as np


class TissueGasExchangeModel:
    """
    Tissue Gas Exchange Model - Albanese 2016 Equations A57-A66

    Handles O2 and CO2 exchange in peripheral tissue beds:
    - Coronary (heart) - A57, A58
    - Brain - A59, A60
    - Active muscle - A61, A62 (Magosso extension)
    - Resting muscle - A61, A62 (Magosso extension)
    - Extrasplanchnic - A63, A64
    - Splanchnic - A65, A66

    Note: Albanese has single muscle compartment, but Magosso splits into
    active (exercising) and resting muscle for exercise simulations

    States: Chp_O2, Chp_CO2, Cbp_O2, Cbp_CO2, Camp_O2, Camp_CO2,
            Crmp_O2, Crmp_CO2, Cep_O2, Cep_CO2, Csp_O2, Csp_CO2 (12)
    """

    def __init__(self, params):
        """
        Initialize tissue gas exchange model

        Parameters dict should contain:
        - Tissue volumes: VT_hp, VT_bp, VT_amp, VT_rmp, VT_ep, VT_sp
        - Metabolic rates: MO2_hp, MCO2_hp, MO2_bp, MCO2_bp, etc.
        """
        # Store parameters
        self.params = params

        # Tissue volumes (includes blood + extravascular fluid)
        self.VT_hp = params['VT_hp']  # Coronary tissue
        self.VT_bp = params['VT_bp']  # Brain tissue
        self.VT_amp = params['VT_amp']  # Active muscle tissue
        self.VT_rmp = params['VT_rmp']  # Resting muscle tissue
        self.VT_ep = params['VT_ep']  # Extrasplanchnic tissue
        self.VT_sp = params['VT_sp']  # Splanchnic tissue

        # Metabolic rates (can be updated during exercise)
        self.MO2_hp = params['MO2_hp']  # Coronary O2 consumption
        self.MCO2_hp = params['MCO2_hp']  # Coronary CO2 production
        self.MO2_bp = params['MO2_bp']  # Brain O2 consumption
        self.MCO2_bp = params['MCO2_bp']  # Brain CO2 production
        self.MO2_amp = params['MO2_amp']  # Active muscle O2 consumption
        self.MCO2_amp = params['MCO2_amp']  # Active muscle CO2 production
        self.MO2_rmp = params['MO2_rmp']  # Resting muscle O2 consumption
        self.MCO2_rmp = params['MCO2_rmp']  # Resting muscle CO2 production
        self.MO2_ep = params['MO2_ep']  # Extrasplanchnic O2 consumption
        self.MCO2_ep = params['MCO2_ep']  # Extrasplanchnic CO2 production
        self.MO2_sp = params['MO2_sp']  # Splanchnic O2 consumption
        self.MCO2_sp = params['MCO2_sp']  # Splanchnic CO2 production

    def coronaryO2(self, Chp_O2, Vhp, Qhp_in, Ca_O2):
        """
        Coronary O2 exchange (A57)
        (VT,hp + Vhp) · dChp,O2/dt = Qhp,in · (Ca,O2 - Chp,O2) - MO2,hp

        Parameters:
        - Chp_O2: coronary tissue O2 concentration
        - Vhp: coronary peripheral blood volume
        - Qhp_in: coronary blood flow
        - Ca_O2: arterial O2 concentration

        Returns:
        - dChp_O2: concentration derivative
        """
        dChp_O2 = (Qhp_in * (Ca_O2 - Chp_O2) - self.MO2_hp) / (self.VT_hp + Vhp)
        return dChp_O2

    def coronaryCO2(self, Chp_CO2, Vhp, Qhp_in, Ca_CO2):
        """
        Coronary CO2 exchange (A58)
        (VT,hp + Vhp) · dChp,CO2/dt = Qhp,in · (Ca,CO2 - Chp,CO2) + MCO2,hp

        Parameters:
        - Chp_CO2: coronary tissue CO2 concentration
        - Vhp: coronary peripheral blood volume
        - Qhp_in: coronary blood flow
        - Ca_CO2: arterial CO2 concentration

        Returns:
        - dChp_CO2: concentration derivative
        """
        dChp_CO2 = (Qhp_in * (Ca_CO2 - Chp_CO2) + self.MCO2_hp) / (self.VT_hp + Vhp)
        return dChp_CO2

    def brainO2(self, Cbp_O2, Vbp, Qbp_in, Ca_O2):
        """
        Brain O2 exchange (A59)
        (VT,bp + Vbp) · dCbp,O2/dt = Qbp,in · (Ca,O2 - Cbp,O2) - MO2,bp

        Parameters:
        - Cbp_O2: brain tissue O2 concentration
        - Vbp: brain peripheral blood volume
        - Qbp_in: brain blood flow
        - Ca_O2: arterial O2 concentration

        Returns:
        - dCbp_O2: concentration derivative
        """
        dCbp_O2 = (Qbp_in * (Ca_O2 - Cbp_O2) - self.MO2_bp) / (self.VT_bp + Vbp)
        return dCbp_O2

    def brainCO2(self, Cbp_CO2, Vbp, Qbp_in, Ca_CO2):
        """
        Brain CO2 exchange (A60)
        (VT,bp + Vbp) · dCbp,CO2/dt = Qbp,in · (Ca,CO2 - Cbp,CO2) + MCO2,bp

        Parameters:
        - Cbp_CO2: brain tissue CO2 concentration
        - Vbp: brain peripheral blood volume
        - Qbp_in: brain blood flow
        - Ca_CO2: arterial CO2 concentration

        Returns:
        - dCbp_CO2: concentration derivative
        """
        dCbp_CO2 = (Qbp_in * (Ca_CO2 - Cbp_CO2) + self.MCO2_bp) / (self.VT_bp + Vbp)
        return dCbp_CO2

    def activeMuscleO2(self, Camp_O2, Vamp, Qamp_in, Ca_O2):
        """
        Active muscle O2 exchange (A61 - Magosso extension)
        (VT,amp + Vamp) · dCamp,O2/dt = Qamp,in · (Ca,O2 - Camp,O2) - MO2,amp

        Parameters:
        - Camp_O2: active muscle tissue O2 concentration
        - Vamp: active muscle peripheral blood volume
        - Qamp_in: active muscle blood flow
        - Ca_O2: arterial O2 concentration

        Returns:
        - dCamp_O2: concentration derivative
        """
        dCamp_O2 = (Qamp_in * (Ca_O2 - Camp_O2) - self.MO2_amp) / (self.VT_amp + Vamp)
        return dCamp_O2

    def activeMuscleCO2(self, Camp_CO2, Vamp, Qamp_in, Ca_CO2):
        """
        Active muscle CO2 exchange (A62 - Magosso extension)
        (VT,amp + Vamp) · dCamp,CO2/dt = Qamp,in · (Ca,CO2 - Camp,CO2) + MCO2,amp

        Parameters:
        - Camp_CO2: active muscle tissue CO2 concentration
        - Vamp: active muscle peripheral blood volume
        - Qamp_in: active muscle blood flow
        - Ca_CO2: arterial CO2 concentration

        Returns:
        - dCamp_CO2: concentration derivative
        """
        dCamp_CO2 = (Qamp_in * (Ca_CO2 - Camp_CO2) + self.MCO2_amp) / (self.VT_amp + Vamp)
        return dCamp_CO2

    def restingMuscleO2(self, Crmp_O2, Vrmp, Qrmp_in, Ca_O2):
        """
        Resting muscle O2 exchange (A61 - Magosso extension)
        (VT,rmp + Vrmp) · dCrmp,O2/dt = Qrmp,in · (Ca,O2 - Crmp,O2) - MO2,rmp

        Parameters:
        - Crmp_O2: resting muscle tissue O2 concentration
        - Vrmp: resting muscle peripheral blood volume
        - Qrmp_in: resting muscle blood flow
        - Ca_O2: arterial O2 concentration

        Returns:
        - dCrmp_O2: concentration derivative
        """
        dCrmp_O2 = (Qrmp_in * (Ca_O2 - Crmp_O2) - self.MO2_rmp) / (self.VT_rmp + Vrmp)
        return dCrmp_O2

    def restingMuscleCO2(self, Crmp_CO2, Vrmp, Qrmp_in, Ca_CO2):
        """
        Resting muscle CO2 exchange (A62 - Magosso extension)
        (VT,rmp + Vrmp) · dCrmp,CO2/dt = Qrmp,in · (Ca,CO2 - Crmp,CO2) + MCO2,rmp

        Parameters:
        - Crmp_CO2: resting muscle tissue CO2 concentration
        - Vrmp: resting muscle peripheral blood volume
        - Qrmp_in: resting muscle blood flow
        - Ca_CO2: arterial CO2 concentration

        Returns:
        - dCrmp_CO2: concentration derivative
        """
        dCrmp_CO2 = (Qrmp_in * (Ca_CO2 - Crmp_CO2) + self.MCO2_rmp) / (self.VT_rmp + Vrmp)
        return dCrmp_CO2

    def extrasplanchnicO2(self, Cep_O2, Vep, Qep_in, Ca_O2):
        """
        Extrasplanchnic O2 exchange (A63)
        (VT,ep + Vep) · dCep,O2/dt = Qep,in · (Ca,O2 - Cep,O2) - MO2,ep

        Parameters:
        - Cep_O2: extrasplanchnic tissue O2 concentration
        - Vep: extrasplanchnic peripheral blood volume
        - Qep_in: extrasplanchnic blood flow
        - Ca_O2: arterial O2 concentration

        Returns:
        - dCep_O2: concentration derivative
        """
        dCep_O2 = (Qep_in * (Ca_O2 - Cep_O2) - self.MO2_ep) / (self.VT_ep + Vep)
        return dCep_O2

    def extrasplanchnicCO2(self, Cep_CO2, Vep, Qep_in, Ca_CO2):
        """
        Extrasplanchnic CO2 exchange (A64)
        (VT,ep + Vep) · dCep,CO2/dt = Qep,in · (Ca,CO2 - Cep,CO2) + MCO2,ep

        Parameters:
        - Cep_CO2: extrasplanchnic tissue CO2 concentration
        - Vep: extrasplanchnic peripheral blood volume
        - Qep_in: extrasplanchnic blood flow
        - Ca_CO2: arterial CO2 concentration

        Returns:
        - dCep_CO2: concentration derivative
        """
        dCep_CO2 = (Qep_in * (Ca_CO2 - Cep_CO2) + self.MCO2_ep) / (self.VT_ep + Vep)
        return dCep_CO2

    def splanchnicO2(self, Csp_O2, Vsp, Qsp_in, Ca_O2):
        """
        Splanchnic O2 exchange (A65)
        (VT,sp + Vsp) · dCsp,O2/dt = Qsp,in · (Ca,O2 - Csp,O2) - MO2,sp

        Parameters:
        - Csp_O2: splanchnic tissue O2 concentration
        - Vsp: splanchnic peripheral blood volume
        - Qsp_in: splanchnic blood flow
        - Ca_O2: arterial O2 concentration

        Returns:
        - dCsp_O2: concentration derivative
        """
        dCsp_O2 = (Qsp_in * (Ca_O2 - Csp_O2) - self.MO2_sp) / (self.VT_sp + Vsp)
        return dCsp_O2

    def splanchnicCO2(self, Csp_CO2, Vsp, Qsp_in, Ca_CO2):
        """
        Splanchnic CO2 exchange (A66)
        (VT,sp + Vsp) · dCsp,CO2/dt = Qsp,in · (Ca,CO2 - Csp,CO2) + MCO2,sp

        Parameters:
        - Csp_CO2: splanchnic tissue CO2 concentration
        - Vsp: splanchnic peripheral blood volume
        - Qsp_in: splanchnic blood flow
        - Ca_CO2: arterial CO2 concentration

        Returns:
        - dCsp_CO2: concentration derivative
        """
        dCsp_CO2 = (Qsp_in * (Ca_CO2 - Csp_CO2) + self.MCO2_sp) / (self.VT_sp + Vsp)
        return dCsp_CO2

    def update_metabolic_rates(self, MO2_dict=None, MCO2_dict=None):
        """
        Update metabolic rates (useful for exercise simulations)

        Parameters:
        - MO2_dict: dict with keys like 'hp', 'bp', 'amp', 'rmp', 'ep', 'sp'
        - MCO2_dict: dict with keys like 'hp', 'bp', 'amp', 'rmp', 'ep', 'sp'
        """
        if MO2_dict is not None:
            if 'hp' in MO2_dict: self.MO2_hp = MO2_dict['hp']
            if 'bp' in MO2_dict: self.MO2_bp = MO2_dict['bp']
            if 'amp' in MO2_dict: self.MO2_amp = MO2_dict['amp']
            if 'rmp' in MO2_dict: self.MO2_rmp = MO2_dict['rmp']
            if 'ep' in MO2_dict: self.MO2_ep = MO2_dict['ep']
            if 'sp' in MO2_dict: self.MO2_sp = MO2_dict['sp']

        if MCO2_dict is not None:
            if 'hp' in MCO2_dict: self.MCO2_hp = MCO2_dict['hp']
            if 'bp' in MCO2_dict: self.MCO2_bp = MCO2_dict['bp']
            if 'amp' in MCO2_dict: self.MCO2_amp = MCO2_dict['amp']
            if 'rmp' in MCO2_dict: self.MCO2_rmp = MCO2_dict['rmp']
            if 'ep' in MCO2_dict: self.MCO2_ep = MCO2_dict['ep']
            if 'sp' in MCO2_dict: self.MCO2_sp = MCO2_dict['sp']

    # =========================================================================
    # MASTER COMPUTE DERIVATIVES
    # =========================================================================

    def compute_derivatives(self, t, Chp_O2, Chp_CO2, Cbp_O2, Cbp_CO2, Camp_O2, Camp_CO2,
                            Crmp_O2, Crmp_CO2, Cep_O2, Cep_CO2, Csp_O2, Csp_CO2,
                            Vhp, Vbp, Vamp, Vrmp, Vep, Vsp,
                            Qhp, Qbp, Qamp, Qrmp, Qep, Qsp,
                            Ca_O2, Ca_CO2):
        """
        Compute all tissue gas exchange derivatives for Euler integration

        Albanese 2016 Equations A57-A66

        State variables (passed in):
        - Chp_O2, Chp_CO2: coronary tissue O2/CO2 concentrations
        - Cbp_O2, Cbp_CO2: brain tissue O2/CO2 concentrations
        - Camp_O2, Camp_CO2: active muscle tissue O2/CO2 concentrations
        - Crmp_O2, Crmp_CO2: resting muscle tissue O2/CO2 concentrations
        - Cep_O2, Cep_CO2: extrasplanchnic tissue O2/CO2 concentrations
        - Csp_O2, Csp_CO2: splanchnic tissue O2/CO2 concentrations

        Coupling inputs (from SystemicModel):
        - Vhp, Vbp, Vamp, Vrmp, Vep, Vsp: peripheral blood volumes
        - Qhp, Qbp, Qamp, Qrmp, Qep, Qsp: peripheral blood flows

        Coupling inputs (from LungGasTransferModel):
        - Ca_O2: arterial O2 concentration
        - Ca_CO2: arterial CO2 concentration

        Returns:
        - derivatives: dict with all concentration derivatives
        - outputs: dict with venous concentrations for each bed
        """

        # 1. Coronary (A57, A58)
        dChp_O2 = self.coronaryO2(Chp_O2, Vhp, Qhp, Ca_O2)
        dChp_CO2 = self.coronaryCO2(Chp_CO2, Vhp, Qhp, Ca_CO2)

        # 2. Brain (A59, A60)
        dCbp_O2 = self.brainO2(Cbp_O2, Vbp, Qbp, Ca_O2)
        dCbp_CO2 = self.brainCO2(Cbp_CO2, Vbp, Qbp, Ca_CO2)

        # 3. Active muscle (A61, A62)
        dCamp_O2 = self.activeMuscleO2(Camp_O2, Vamp, Qamp, Ca_O2)
        dCamp_CO2 = self.activeMuscleCO2(Camp_CO2, Vamp, Qamp, Ca_CO2)

        # 4. Resting muscle (A61, A62)
        dCrmp_O2 = self.restingMuscleO2(Crmp_O2, Vrmp, Qrmp, Ca_O2)
        dCrmp_CO2 = self.restingMuscleCO2(Crmp_CO2, Vrmp, Qrmp, Ca_CO2)

        # 5. Extrasplanchnic (A63, A64)
        dCep_O2 = self.extrasplanchnicO2(Cep_O2, Vep, Qep, Ca_O2)
        dCep_CO2 = self.extrasplanchnicCO2(Cep_CO2, Vep, Qep, Ca_CO2)

        # 6. Splanchnic (A65, A66)
        dCsp_O2 = self.splanchnicO2(Csp_O2, Vsp, Qsp, Ca_O2)
        dCsp_CO2 = self.splanchnicCO2(Csp_CO2, Vsp, Qsp, Ca_CO2)

        # Package derivatives
        derivatives = {
            'dChp_O2': dChp_O2,
            'dChp_CO2': dChp_CO2,
            'dCbp_O2': dCbp_O2,
            'dCbp_CO2': dCbp_CO2,
            'dCamp_O2': dCamp_O2,
            'dCamp_CO2': dCamp_CO2,
            'dCrmp_O2': dCrmp_O2,
            'dCrmp_CO2': dCrmp_CO2,
            'dCep_O2': dCep_O2,
            'dCep_CO2': dCep_CO2,
            'dCsp_O2': dCsp_O2,
            'dCsp_CO2': dCsp_CO2
        }

        # Package outputs (tissue concentrations = venous concentrations)
        outputs = {
            'Chp_O2': Chp_O2,
            'Chp_CO2': Chp_CO2,
            'Cbp_O2': Cbp_O2,
            'Cbp_CO2': Cbp_CO2,
            'Camp_O2': Camp_O2,
            'Camp_CO2': Camp_CO2,
            'Crmp_O2': Crmp_O2,
            'Crmp_CO2': Crmp_CO2,
            'Cep_O2': Cep_O2,
            'Cep_CO2': Cep_CO2,
            'Csp_O2': Csp_O2,
            'Csp_CO2': Csp_CO2
        }

        return derivatives, outputs