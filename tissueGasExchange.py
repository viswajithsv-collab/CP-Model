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
    """

    def __init__(self, params):
        """
        Initialize tissue gas exchange model

        Parameters dict should contain:
        - Tissue volumes: VT_hp, VT_bp, VT_amp, VT_rmp, VT_ep, VT_sp
        - Metabolic rates: MO2_hp, MCO2_hp, MO2_bp, MCO2_bp, etc.
        - Initial concentrations: Chp_O2_init, Chp_CO2_init, etc.
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

        # Initialize state variables (tissue concentrations)
        self.Chp_O2 = params.get('Chp_O2_init', 150.0)  # Coronary O2
        self.Chp_CO2 = params.get('Chp_CO2_init', 500.0)  # Coronary CO2
        self.Cbp_O2 = params.get('Cbp_O2_init', 150.0)  # Brain O2
        self.Cbp_CO2 = params.get('Cbp_CO2_init', 500.0)  # Brain CO2
        self.Camp_O2 = params.get('Camp_O2_init', 150.0)  # Active muscle O2
        self.Camp_CO2 = params.get('Camp_CO2_init', 500.0)  # Active muscle CO2
        self.Crmp_O2 = params.get('Crmp_O2_init', 150.0)  # Resting muscle O2
        self.Crmp_CO2 = params.get('Crmp_CO2_init', 500.0)  # Resting muscle CO2
        self.Cep_O2 = params.get('Cep_O2_init', 150.0)  # Extrasplanchnic O2
        self.Cep_CO2 = params.get('Cep_CO2_init', 500.0)  # Extrasplanchnic CO2
        self.Csp_O2 = params.get('Csp_O2_init', 150.0)  # Splanchnic O2
        self.Csp_CO2 = params.get('Csp_CO2_init', 500.0)  # Splanchnic CO2

    def coronaryO2(self, Vhp, Qhp_in, Ca_O2, dt):
        """
        Coronary O2 exchange (A57)
        (VT,hp + Vhp) · dChp,O2/dt = Qhp,in · (Ca,O2 - Chp,O2) - MO2,hp

        Parameters:
        - Vhp: coronary peripheral blood volume
        - Qhp_in: coronary blood flow
        - Ca_O2: arterial O2 concentration
        - dt: time step

        Returns:
        - Chp_O2_new: updated concentration
        - dChp_O2: concentration derivative
        """
        dChp_O2 = (Qhp_in * (Ca_O2 - self.Chp_O2) - self.MO2_hp) / (self.VT_hp + Vhp)
        Chp_O2_new = self.Chp_O2 + dChp_O2 * dt
        return Chp_O2_new, dChp_O2

    def coronaryCO2(self, Vhp, Qhp_in, Ca_CO2, dt):
        """
        Coronary CO2 exchange (A58)
        (VT,hp + Vhp) · dChp,CO2/dt = Qhp,in · (Ca,CO2 - Chp,CO2) + MCO2,hp

        Parameters:
        - Vhp: coronary peripheral blood volume
        - Qhp_in: coronary blood flow
        - Ca_CO2: arterial CO2 concentration
        - dt: time step

        Returns:
        - Chp_CO2_new: updated concentration
        - dChp_CO2: concentration derivative
        """
        dChp_CO2 = (Qhp_in * (Ca_CO2 - self.Chp_CO2) + self.MCO2_hp) / (self.VT_hp + Vhp)
        Chp_CO2_new = self.Chp_CO2 + dChp_CO2 * dt
        return Chp_CO2_new, dChp_CO2

    def brainO2(self, Vbp, Qbp_in, Ca_O2, dt):
        """
        Brain O2 exchange (A59)
        (VT,bp + Vbp) · dCbp,O2/dt = Qbp,in · (Ca,O2 - Cbp,O2) - MO2,bp

        Parameters:
        - Vbp: brain peripheral blood volume
        - Qbp_in: brain blood flow
        - Ca_O2: arterial O2 concentration
        - dt: time step

        Returns:
        - Cbp_O2_new: updated concentration
        - dCbp_O2: concentration derivative
        """
        dCbp_O2 = (Qbp_in * (Ca_O2 - self.Cbp_O2) - self.MO2_bp) / (self.VT_bp + Vbp)
        Cbp_O2_new = self.Cbp_O2 + dCbp_O2 * dt
        return Cbp_O2_new, dCbp_O2

    def brainCO2(self, Vbp, Qbp_in, Ca_CO2, dt):
        """
        Brain CO2 exchange (A60)
        (VT,bp + Vbp) · dCbp,CO2/dt = Qbp,in · (Ca,CO2 - Cbp,CO2) + MCO2,bp

        Parameters:
        - Vbp: brain peripheral blood volume
        - Qbp_in: brain blood flow
        - Ca_CO2: arterial CO2 concentration
        - dt: time step

        Returns:
        - Cbp_CO2_new: updated concentration
        - dCbp_CO2: concentration derivative
        """
        dCbp_CO2 = (Qbp_in * (Ca_CO2 - self.Cbp_CO2) + self.MCO2_bp) / (self.VT_bp + Vbp)
        Cbp_CO2_new = self.Cbp_CO2 + dCbp_CO2 * dt
        return Cbp_CO2_new, dCbp_CO2

    def activeMuscleO2(self, Vamp, Qamp_in, Ca_O2, dt):
        """
        Active muscle O2 exchange (A61 - Magosso extension)
        (VT,amp + Vamp) · dCamp,O2/dt = Qamp,in · (Ca,O2 - Camp,O2) - MO2,amp

        Parameters:
        - Vamp: active muscle peripheral blood volume
        - Qamp_in: active muscle blood flow
        - Ca_O2: arterial O2 concentration
        - dt: time step

        Returns:
        - Camp_O2_new: updated concentration
        - dCamp_O2: concentration derivative
        """
        dCamp_O2 = (Qamp_in * (Ca_O2 - self.Camp_O2) - self.MO2_amp) / (self.VT_amp + Vamp)
        Camp_O2_new = self.Camp_O2 + dCamp_O2 * dt
        return Camp_O2_new, dCamp_O2

    def activeMuscleCO2(self, Vamp, Qamp_in, Ca_CO2, dt):
        """
        Active muscle CO2 exchange (A62 - Magosso extension)
        (VT,amp + Vamp) · dCamp,CO2/dt = Qamp,in · (Ca,CO2 - Camp,CO2) + MCO2,amp

        Parameters:
        - Vamp: active muscle peripheral blood volume
        - Qamp_in: active muscle blood flow
        - Ca_CO2: arterial CO2 concentration
        - dt: time step

        Returns:
        - Camp_CO2_new: updated concentration
        - dCamp_CO2: concentration derivative
        """
        dCamp_CO2 = (Qamp_in * (Ca_CO2 - self.Camp_CO2) + self.MCO2_amp) / (self.VT_amp + Vamp)
        Camp_CO2_new = self.Camp_CO2 + dCamp_CO2 * dt
        return Camp_CO2_new, dCamp_CO2

    def restingMuscleO2(self, Vrmp, Qrmp_in, Ca_O2, dt):
        """
        Resting muscle O2 exchange (A61 - Magosso extension)
        (VT,rmp + Vrmp) · dCrmp,O2/dt = Qrmp,in · (Ca,O2 - Crmp,O2) - MO2,rmp

        Parameters:
        - Vrmp: resting muscle peripheral blood volume
        - Qrmp_in: resting muscle blood flow
        - Ca_O2: arterial O2 concentration
        - dt: time step

        Returns:
        - Crmp_O2_new: updated concentration
        - dCrmp_O2: concentration derivative
        """
        dCrmp_O2 = (Qrmp_in * (Ca_O2 - self.Crmp_O2) - self.MO2_rmp) / (self.VT_rmp + Vrmp)
        Crmp_O2_new = self.Crmp_O2 + dCrmp_O2 * dt
        return Crmp_O2_new, dCrmp_O2

    def restingMuscleCO2(self, Vrmp, Qrmp_in, Ca_CO2, dt):
        """
        Resting muscle CO2 exchange (A62 - Magosso extension)
        (VT,rmp + Vrmp) · dCrmp,CO2/dt = Qrmp,in · (Ca,CO2 - Crmp,CO2) + MCO2,rmp

        Parameters:
        - Vrmp: resting muscle peripheral blood volume
        - Qrmp_in: resting muscle blood flow
        - Ca_CO2: arterial CO2 concentration
        - dt: time step

        Returns:
        - Crmp_CO2_new: updated concentration
        - dCrmp_CO2: concentration derivative
        """
        dCrmp_CO2 = (Qrmp_in * (Ca_CO2 - self.Crmp_CO2) + self.MCO2_rmp) / (self.VT_rmp + Vrmp)
        Crmp_CO2_new = self.Crmp_CO2 + dCrmp_CO2 * dt
        return Crmp_CO2_new, dCrmp_CO2

    def extrasplanchnicO2(self, Vep, Qep_in, Ca_O2, dt):
        """
        Extrasplanchnic O2 exchange (A63)
        (VT,ep + Vep) · dCep,O2/dt = Qep,in · (Ca,O2 - Cep,O2) - MO2,ep

        Parameters:
        - Vep: extrasplanchnic peripheral blood volume
        - Qep_in: extrasplanchnic blood flow
        - Ca_O2: arterial O2 concentration
        - dt: time step

        Returns:
        - Cep_O2_new: updated concentration
        - dCep_O2: concentration derivative
        """
        dCep_O2 = (Qep_in * (Ca_O2 - self.Cep_O2) - self.MO2_ep) / (self.VT_ep + Vep)
        Cep_O2_new = self.Cep_O2 + dCep_O2 * dt
        return Cep_O2_new, dCep_O2

    def extrasplanchnicCO2(self, Vep, Qep_in, Ca_CO2, dt):
        """
        Extrasplanchnic CO2 exchange (A64)
        (VT,ep + Vep) · dCep,CO2/dt = Qep,in · (Ca,CO2 - Cep,CO2) + MCO2,ep

        Parameters:
        - Vep: extrasplanchnic peripheral blood volume
        - Qep_in: extrasplanchnic blood flow
        - Ca_CO2: arterial CO2 concentration
        - dt: time step

        Returns:
        - Cep_CO2_new: updated concentration
        - dCep_CO2: concentration derivative
        """
        dCep_CO2 = (Qep_in * (Ca_CO2 - self.Cep_CO2) + self.MCO2_ep) / (self.VT_ep + Vep)
        Cep_CO2_new = self.Cep_CO2 + dCep_CO2 * dt
        return Cep_CO2_new, dCep_CO2

    def splanchnicO2(self, Vsp, Qsp_in, Ca_O2, dt):
        """
        Splanchnic O2 exchange (A65)
        (VT,sp + Vsp) · dCsp,O2/dt = Qsp,in · (Ca,O2 - Csp,O2) - MO2,sp

        Parameters:
        - Vsp: splanchnic peripheral blood volume
        - Qsp_in: splanchnic blood flow
        - Ca_O2: arterial O2 concentration
        - dt: time step

        Returns:
        - Csp_O2_new: updated concentration
        - dCsp_O2: concentration derivative
        """
        dCsp_O2 = (Qsp_in * (Ca_O2 - self.Csp_O2) - self.MO2_sp) / (self.VT_sp + Vsp)
        Csp_O2_new = self.Csp_O2 + dCsp_O2 * dt
        return Csp_O2_new, dCsp_O2

    def splanchnicCO2(self, Vsp, Qsp_in, Ca_CO2, dt):
        """
        Splanchnic CO2 exchange (A66)
        (VT,sp + Vsp) · dCsp,CO2/dt = Qsp,in · (Ca,CO2 - Csp,CO2) + MCO2,sp

        Parameters:
        - Vsp: splanchnic peripheral blood volume
        - Qsp_in: splanchnic blood flow
        - Ca_CO2: arterial CO2 concentration
        - dt: time step

        Returns:
        - Csp_CO2_new: updated concentration
        - dCsp_CO2: concentration derivative
        """
        dCsp_CO2 = (Qsp_in * (Ca_CO2 - self.Csp_CO2) + self.MCO2_sp) / (self.VT_sp + Vsp)
        Csp_CO2_new = self.Csp_CO2 + dCsp_CO2 * dt
        return Csp_CO2_new, dCsp_CO2

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

    def compute_derivatives(self, volumes, flows, Ca_O2, Ca_CO2, dt):
        """
        Compute all tissue gas exchange for one time step

        Parameters:
        - volumes: dict with 'Vhp', 'Vbp', 'Vamp', 'Vrmp', 'Vep', 'Vsp' (from SystemicModel)
        - flows: dict with 'Qhp', 'Qbp', 'Qamp', 'Qrmp', 'Qep', 'Qsp' (from SystemicModel)
        - Ca_O2: arterial O2 concentration (from LungGasTransferModel)
        - Ca_CO2: arterial CO2 concentration (from LungGasTransferModel)
        - dt: time step

        Returns:
        - derivatives: dict with all concentration derivatives
        - outputs: dict with updated concentrations
        """

        # 1. Coronary (A57, A58)
        Chp_O2_new, dChp_O2 = self.coronaryO2(volumes['Vhp'], flows['Qhp'], Ca_O2, dt)
        Chp_CO2_new, dChp_CO2 = self.coronaryCO2(volumes['Vhp'], flows['Qhp'], Ca_CO2, dt)

        # 2. Brain (A59, A60)
        Cbp_O2_new, dCbp_O2 = self.brainO2(volumes['Vbp'], flows['Qbp'], Ca_O2, dt)
        Cbp_CO2_new, dCbp_CO2 = self.brainCO2(volumes['Vbp'], flows['Qbp'], Ca_CO2, dt)

        # 3. Active muscle (A61, A62)
        Camp_O2_new, dCamp_O2 = self.activeMuscleO2(volumes['Vamp'], flows['Qamp'], Ca_O2, dt)
        Camp_CO2_new, dCamp_CO2 = self.activeMuscleCO2(volumes['Vamp'], flows['Qamp'], Ca_CO2, dt)

        # 4. Resting muscle (A61, A62)
        Crmp_O2_new, dCrmp_O2 = self.restingMuscleO2(volumes['Vrmp'], flows['Qrmp'], Ca_O2, dt)
        Crmp_CO2_new, dCrmp_CO2 = self.restingMuscleCO2(volumes['Vrmp'], flows['Qrmp'], Ca_CO2, dt)

        # 5. Extrasplanchnic (A63, A64)
        Cep_O2_new, dCep_O2 = self.extrasplanchnicO2(volumes['Vep'], flows['Qep'], Ca_O2, dt)
        Cep_CO2_new, dCep_CO2 = self.extrasplanchnicCO2(volumes['Vep'], flows['Qep'], Ca_CO2, dt)

        # 6. Splanchnic (A65, A66)
        Csp_O2_new, dCsp_O2 = self.splanchnicO2(volumes['Vsp'], flows['Qsp'], Ca_O2, dt)
        Csp_CO2_new, dCsp_CO2 = self.splanchnicCO2(volumes['Vsp'], flows['Qsp'], Ca_CO2, dt)

        # Update state variables
        self.Chp_O2 = Chp_O2_new
        self.Chp_CO2 = Chp_CO2_new
        self.Cbp_O2 = Cbp_O2_new
        self.Cbp_CO2 = Cbp_CO2_new
        self.Camp_O2 = Camp_O2_new
        self.Camp_CO2 = Camp_CO2_new
        self.Crmp_O2 = Crmp_O2_new
        self.Crmp_CO2 = Crmp_CO2_new
        self.Cep_O2 = Cep_O2_new
        self.Cep_CO2 = Cep_CO2_new
        self.Csp_O2 = Csp_O2_new
        self.Csp_CO2 = Csp_CO2_new

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

        # Package outputs
        outputs = {
            'Chp_O2': self.Chp_O2,
            'Chp_CO2': self.Chp_CO2,
            'Cbp_O2': self.Cbp_O2,
            'Cbp_CO2': self.Cbp_CO2,
            'Camp_O2': self.Camp_O2,
            'Camp_CO2': self.Camp_CO2,
            'Crmp_O2': self.Crmp_O2,
            'Crmp_CO2': self.Crmp_CO2,
            'Cep_O2': self.Cep_O2,
            'Cep_CO2': self.Cep_CO2,
            'Csp_O2': self.Csp_O2,
            'Csp_CO2': self.Csp_CO2
        }

        return derivatives, outputs