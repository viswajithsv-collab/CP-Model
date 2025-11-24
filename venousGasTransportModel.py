import numpy as np


class VenousGasTransportModel:
    """
    Venous Gas Transport Model - Albanese 2016 Equations A67-A78
    
    Handles O2 and CO2 transport in venous blood:
    - Coronary venous - A67, A68
    - Brain venous - A69, A70
    - Active muscle venous - A71, A72 (Magosso extension)
    - Resting muscle venous - A71, A72 (Magosso extension)
    - Extrasplanchnic venous - A73, A74
    - Splanchnic venous - A75, A76
    - Thoracic venous (mixed venous) - A77, A78
    
    Note: Magosso splits muscle into active/resting for exercise
    """
    
    def __init__(self, params):
        """
        Initialize venous gas transport model
        
        Parameters dict should contain:
        - Initial concentrations: Chv_O2_init, Chv_CO2_init, etc. for all 6 venous beds
        - Mixed venous: Cv_O2_init, Cv_CO2_init
        """
        # Store parameters
        self.params = params
        
        # Initialize venous concentration state variables
        self.Chv_O2 = params.get('Chv_O2_init', 140.0)      # Coronary venous O2
        self.Chv_CO2 = params.get('Chv_CO2_init', 520.0)    # Coronary venous CO2
        
        self.Cbv_O2 = params.get('Cbv_O2_init', 140.0)      # Brain venous O2
        self.Cbv_CO2 = params.get('Cbv_CO2_init', 520.0)    # Brain venous CO2
        
        self.Camv_O2 = params.get('Camv_O2_init', 140.0)    # Active muscle venous O2
        self.Camv_CO2 = params.get('Camv_CO2_init', 520.0)  # Active muscle venous CO2
        
        self.Crmv_O2 = params.get('Crmv_O2_init', 140.0)    # Resting muscle venous O2
        self.Crmv_CO2 = params.get('Crmv_CO2_init', 520.0)  # Resting muscle venous CO2
        
        self.Cev_O2 = params.get('Cev_O2_init', 140.0)      # Extrasplanchnic venous O2
        self.Cev_CO2 = params.get('Cev_CO2_init', 520.0)    # Extrasplanchnic venous CO2
        
        self.Csv_O2 = params.get('Csv_O2_init', 140.0)      # Splanchnic venous O2
        self.Csv_CO2 = params.get('Csv_CO2_init', 520.0)    # Splanchnic venous CO2
        
        # Mixed venous (thoracic veins)
        self.Cv_O2 = params.get('Cv_O2_init', 140.0)        # Mixed venous O2
        self.Cv_CO2 = params.get('Cv_CO2_init', 520.0)      # Mixed venous CO2
    
    
    def coronaryVenousO2(self, Vhv, Qhp, Chp_O2, dt):
        """
        Coronary venous O2 transport (A67)
        Vhv · dChv,O2/dt = Qhp · (Chp,O2 - Chv,O2)
        
        Parameters:
        - Vhv: coronary venous volume
        - Qhp: coronary blood flow
        - Chp_O2: coronary tissue O2 concentration
        - dt: time step
        
        Returns:
        - Chv_O2_new: updated concentration
        - dChv_O2: concentration derivative
        """
        dChv_O2 = Qhp * (Chp_O2 - self.Chv_O2) / Vhv
        Chv_O2_new = self.Chv_O2 + dChv_O2 * dt
        return Chv_O2_new, dChv_O2
    
    
    def coronaryVenousCO2(self, Vhv, Qhp, Chp_CO2, dt):
        """
        Coronary venous CO2 transport (A68)
        Vhv · dChv,CO2/dt = Qhp · (Chp,CO2 - Chv,CO2)
        
        Parameters:
        - Vhv: coronary venous volume
        - Qhp: coronary blood flow
        - Chp_CO2: coronary tissue CO2 concentration
        - dt: time step
        
        Returns:
        - Chv_CO2_new: updated concentration
        - dChv_CO2: concentration derivative
        """
        dChv_CO2 = Qhp * (Chp_CO2 - self.Chv_CO2) / Vhv
        Chv_CO2_new = self.Chv_CO2 + dChv_CO2 * dt
        return Chv_CO2_new, dChv_CO2
    
    
    def brainVenousO2(self, Vbv, Qbp, Cbp_O2, dt):
        """
        Brain venous O2 transport (A69)
        Vbv · dCbv,O2/dt = Qbp · (Cbp,O2 - Cbv,O2)
        
        Parameters:
        - Vbv: brain venous volume
        - Qbp: brain blood flow
        - Cbp_O2: brain tissue O2 concentration
        - dt: time step
        
        Returns:
        - Cbv_O2_new: updated concentration
        - dCbv_O2: concentration derivative
        """
        dCbv_O2 = Qbp * (Cbp_O2 - self.Cbv_O2) / Vbv
        Cbv_O2_new = self.Cbv_O2 + dCbv_O2 * dt
        return Cbv_O2_new, dCbv_O2
    
    
    def brainVenousCO2(self, Vbv, Qbp, Cbp_CO2, dt):
        """
        Brain venous CO2 transport (A70)
        Vbv · dCbv,CO2/dt = Qbp · (Cbp,CO2 - Cbv,CO2)
        
        Parameters:
        - Vbv: brain venous volume
        - Qbp: brain blood flow
        - Cbp_CO2: brain tissue CO2 concentration
        - dt: time step
        
        Returns:
        - Cbv_CO2_new: updated concentration
        - dCbv_CO2: concentration derivative
        """
        dCbv_CO2 = Qbp * (Cbp_CO2 - self.Cbv_CO2) / Vbv
        Cbv_CO2_new = self.Cbv_CO2 + dCbv_CO2 * dt
        return Cbv_CO2_new, dCbv_CO2
    
    
    def activeMuscleVenousO2(self, Vamv, Qamp, Camp_O2, dt):
        """
        Active muscle venous O2 transport (A71)
        Vamv · dCamv,O2/dt = Qamp · (Camp,O2 - Camv,O2)
        
        Parameters:
        - Vamv: active muscle venous volume
        - Qamp: active muscle blood flow
        - Camp_O2: active muscle tissue O2 concentration
        - dt: time step
        
        Returns:
        - Camv_O2_new: updated concentration
        - dCamv_O2: concentration derivative
        """
        dCamv_O2 = Qamp * (Camp_O2 - self.Camv_O2) / Vamv
        Camv_O2_new = self.Camv_O2 + dCamv_O2 * dt
        return Camv_O2_new, dCamv_O2
    
    
    def activeMuscleVenousCO2(self, Vamv, Qamp, Camp_CO2, dt):
        """
        Active muscle venous CO2 transport (A72)
        Vamv · dCamv,CO2/dt = Qamp · (Camp,CO2 - Camv,CO2)
        
        Parameters:
        - Vamv: active muscle venous volume
        - Qamp: active muscle blood flow
        - Camp_CO2: active muscle tissue CO2 concentration
        - dt: time step
        
        Returns:
        - Camv_CO2_new: updated concentration
        - dCamv_CO2: concentration derivative
        """
        dCamv_CO2 = Qamp * (Camp_CO2 - self.Camv_CO2) / Vamv
        Camv_CO2_new = self.Camv_CO2 + dCamv_CO2 * dt
        return Camv_CO2_new, dCamv_CO2
    
    
    def restingMuscleVenousO2(self, Vrmv, Qrmp, Crmp_O2, dt):
        """
        Resting muscle venous O2 transport (A71 variant)
        Vrmv · dCrmv,O2/dt = Qrmp · (Crmp,O2 - Crmv,O2)
        
        Parameters:
        - Vrmv: resting muscle venous volume
        - Qrmp: resting muscle blood flow
        - Crmp_O2: resting muscle tissue O2 concentration
        - dt: time step
        
        Returns:
        - Crmv_O2_new: updated concentration
        - dCrmv_O2: concentration derivative
        """
        dCrmv_O2 = Qrmp * (Crmp_O2 - self.Crmv_O2) / Vrmv
        Crmv_O2_new = self.Crmv_O2 + dCrmv_O2 * dt
        return Crmv_O2_new, dCrmv_O2
    
    
    def restingMuscleVenousCO2(self, Vrmv, Qrmp, Crmp_CO2, dt):
        """
        Resting muscle venous CO2 transport (A72 variant)
        Vrmv · dCrmv,CO2/dt = Qrmp · (Crmp,CO2 - Crmv,CO2)
        
        Parameters:
        - Vrmv: resting muscle venous volume
        - Qrmp: resting muscle blood flow
        - Crmp_CO2: resting muscle tissue CO2 concentration
        - dt: time step
        
        Returns:
        - Crmv_CO2_new: updated concentration
        - dCrmv_CO2: concentration derivative
        """
        dCrmv_CO2 = Qrmp * (Crmp_CO2 - self.Crmv_CO2) / Vrmv
        Crmv_CO2_new = self.Crmv_CO2 + dCrmv_CO2 * dt
        return Crmv_CO2_new, dCrmv_CO2
    
    
    def extrasplanchnicVenousO2(self, Vev, Qep, Cep_O2, dt):
        """
        Extrasplanchnic venous O2 transport (A73)
        Vev · dCev,O2/dt = Qep · (Cep,O2 - Cev,O2)
        
        Parameters:
        - Vev: extrasplanchnic venous volume
        - Qep: extrasplanchnic blood flow
        - Cep_O2: extrasplanchnic tissue O2 concentration
        - dt: time step
        
        Returns:
        - Cev_O2_new: updated concentration
        - dCev_O2: concentration derivative
        """
        dCev_O2 = Qep * (Cep_O2 - self.Cev_O2) / Vev
        Cev_O2_new = self.Cev_O2 + dCev_O2 * dt
        return Cev_O2_new, dCev_O2
    
    
    def extrasplanchnicVenousCO2(self, Vev, Qep, Cep_CO2, dt):
        """
        Extrasplanchnic venous CO2 transport (A74)
        Vev · dCev,CO2/dt = Qep · (Cep,CO2 - Cev,CO2)
        
        Parameters:
        - Vev: extrasplanchnic venous volume
        - Qep: extrasplanchnic blood flow
        - Cep_CO2: extrasplanchnic tissue CO2 concentration
        - dt: time step
        
        Returns:
        - Cev_CO2_new: updated concentration
        - dCev_CO2: concentration derivative
        """
        dCev_CO2 = Qep * (Cep_CO2 - self.Cev_CO2) / Vev
        Cev_CO2_new = self.Cev_CO2 + dCev_CO2 * dt
        return Cev_CO2_new, dCev_CO2
    
    
    def splanchnicVenousO2(self, Vsv, Qsp, Csp_O2, dt):
        """
        Splanchnic venous O2 transport (A75)
        Vsv · dCsv,O2/dt = Qsp · (Csp,O2 - Csv,O2)
        
        Parameters:
        - Vsv: splanchnic venous volume
        - Qsp: splanchnic blood flow
        - Csp_O2: splanchnic tissue O2 concentration
        - dt: time step
        
        Returns:
        - Csv_O2_new: updated concentration
        - dCsv_O2: concentration derivative
        """
        dCsv_O2 = Qsp * (Csp_O2 - self.Csv_O2) / Vsv
        Csv_O2_new = self.Csv_O2 + dCsv_O2 * dt
        return Csv_O2_new, dCsv_O2
    
    
    def splanchnicVenousCO2(self, Vsv, Qsp, Csp_CO2, dt):
        """
        Splanchnic venous CO2 transport (A76)
        Vsv · dCsv,CO2/dt = Qsp · (Csp,CO2 - Csv,CO2)
        
        Parameters:
        - Vsv: splanchnic venous volume
        - Qsp: splanchnic blood flow
        - Csp_CO2: splanchnic tissue CO2 concentration
        - dt: time step
        
        Returns:
        - Csv_CO2_new: updated concentration
        - dCsv_CO2: concentration derivative
        """
        dCsv_CO2 = Qsp * (Csp_CO2 - self.Csv_CO2) / Vsv
        Csv_CO2_new = self.Csv_CO2 + dCsv_CO2 * dt
        return Csv_CO2_new, dCsv_CO2
    
    
    def thoracicVenousO2(self, Vtv, Qhv, Qbv, Qamv, Qrmv, Qev, Qsv, dt):
        """
        Thoracic venous O2 mixing (A77) - ALL 6 VENOUS BEDS
        
        Vtv · dCv,O2/dt = Qhv·(Chv,O2 - Cv,O2) + Qbv·(Cbv,O2 - Cv,O2) 
                         + Qamv·(Camv,O2 - Cv,O2) + Qrmv·(Crmv,O2 - Cv,O2)
                         + Qev·(Cev,O2 - Cv,O2) + Qsv·(Csv,O2 - Cv,O2)
        
        Parameters:
        - Vtv: thoracic venous volume
        - Qhv, Qbv, Qamv, Qrmv, Qev, Qsv: venous flows from all 6 beds
        - dt: time step
        
        Returns:
        - Cv_O2_new: updated mixed venous O2 concentration
        - dCv_O2: concentration derivative
        """
        dCv_O2 = (Qhv * (self.Chv_O2 - self.Cv_O2) + 
                  Qbv * (self.Cbv_O2 - self.Cv_O2) +
                  Qamv * (self.Camv_O2 - self.Cv_O2) + 
                  Qrmv * (self.Crmv_O2 - self.Cv_O2) +
                  Qev * (self.Cev_O2 - self.Cv_O2) + 
                  Qsv * (self.Csv_O2 - self.Cv_O2)) / Vtv
        
        Cv_O2_new = self.Cv_O2 + dCv_O2 * dt
        return Cv_O2_new, dCv_O2
    
    
    def thoracicVenousCO2(self, Vtv, Qhv, Qbv, Qamv, Qrmv, Qev, Qsv, dt):
        """
        Thoracic venous CO2 mixing (A78) - ALL 6 VENOUS BEDS
        
        Vtv · dCv,CO2/dt = Qhv·(Chv,CO2 - Cv,CO2) + Qbv·(Cbv,CO2 - Cv,CO2)
                          + Qamv·(Camv,CO2 - Cv,CO2) + Qrmv·(Crmv,CO2 - Cv,CO2)
                          + Qev·(Cev,CO2 - Cv,CO2) + Qsv·(Csv,CO2 - Cv,CO2)
        
        Parameters:
        - Vtv: thoracic venous volume
        - Qhv, Qbv, Qamv, Qrmv, Qev, Qsv: venous flows from all 6 beds
        - dt: time step
        
        Returns:
        - Cv_CO2_new: updated mixed venous CO2 concentration
        - dCv_CO2: concentration derivative
        """
        dCv_CO2 = (Qhv * (self.Chv_CO2 - self.Cv_CO2) + 
                   Qbv * (self.Cbv_CO2 - self.Cv_CO2) +
                   Qamv * (self.Camv_CO2 - self.Cv_CO2) + 
                   Qrmv * (self.Crmv_CO2 - self.Cv_CO2) +
                   Qev * (self.Cev_CO2 - self.Cv_CO2) + 
                   Qsv * (self.Csv_CO2 - self.Cv_CO2)) / Vtv
        
        Cv_CO2_new = self.Cv_CO2 + dCv_CO2 * dt
        return Cv_CO2_new, dCv_CO2
    
    
    def compute_derivatives(self, volumes, flows, tissue_concentrations, dt):
        """
        Compute all venous gas transport for one time step
        
        Parameters:
        - volumes: dict with 'Vhv', 'Vbv', 'Vamv', 'Vrmv', 'Vev', 'Vsv', 'Vtv'
        - flows: dict with 'Qhp', 'Qbp', 'Qamp', 'Qrmp', 'Qep', 'Qsp', 'Qhv', 'Qbv', 'Qamv', 'Qrmv', 'Qev', 'Qsv'
        - tissue_concentrations: dict with tissue O2/CO2 from TissueGasExchangeModel
        - dt: time step
        
        Returns:
        - derivatives: dict with all concentration derivatives
        - outputs: dict with updated concentrations
        """
        
        # 1. Individual venous beds (A67-A76)
        Chv_O2_new, dChv_O2 = self.coronaryVenousO2(
            volumes['Vhv'], flows['Qhp'], tissue_concentrations['Chp_O2'], dt
        )
        Chv_CO2_new, dChv_CO2 = self.coronaryVenousCO2(
            volumes['Vhv'], flows['Qhp'], tissue_concentrations['Chp_CO2'], dt
        )
        
        Cbv_O2_new, dCbv_O2 = self.brainVenousO2(
            volumes['Vbv'], flows['Qbp'], tissue_concentrations['Cbp_O2'], dt
        )
        Cbv_CO2_new, dCbv_CO2 = self.brainVenousCO2(
            volumes['Vbv'], flows['Qbp'], tissue_concentrations['Cbp_CO2'], dt
        )
        
        Camv_O2_new, dCamv_O2 = self.activeMuscleVenousO2(
            volumes['Vamv'], flows['Qamp'], tissue_concentrations['Camp_O2'], dt
        )
        Camv_CO2_new, dCamv_CO2 = self.activeMuscleVenousCO2(
            volumes['Vamv'], flows['Qamp'], tissue_concentrations['Camp_CO2'], dt
        )
        
        Crmv_O2_new, dCrmv_O2 = self.restingMuscleVenousO2(
            volumes['Vrmv'], flows['Qrmp'], tissue_concentrations['Crmp_O2'], dt
        )
        Crmv_CO2_new, dCrmv_CO2 = self.restingMuscleVenousCO2(
            volumes['Vrmv'], flows['Qrmp'], tissue_concentrations['Crmp_CO2'], dt
        )
        
        Cev_O2_new, dCev_O2 = self.extrasplanchnicVenousO2(
            volumes['Vev'], flows['Qep'], tissue_concentrations['Cep_O2'], dt
        )
        Cev_CO2_new, dCev_CO2 = self.extrasplanchnicVenousCO2(
            volumes['Vev'], flows['Qep'], tissue_concentrations['Cep_CO2'], dt
        )
        
        Csv_O2_new, dCsv_O2 = self.splanchnicVenousO2(
            volumes['Vsv'], flows['Qsp'], tissue_concentrations['Csp_O2'], dt
        )
        Csv_CO2_new, dCsv_CO2 = self.splanchnicVenousCO2(
            volumes['Vsv'], flows['Qsp'], tissue_concentrations['Csp_CO2'], dt
        )
        
        # Update individual bed states
        self.Chv_O2 = Chv_O2_new
        self.Chv_CO2 = Chv_CO2_new
        self.Cbv_O2 = Cbv_O2_new
        self.Cbv_CO2 = Cbv_CO2_new
        self.Camv_O2 = Camv_O2_new
        self.Camv_CO2 = Camv_CO2_new
        self.Crmv_O2 = Crmv_O2_new
        self.Crmv_CO2 = Crmv_CO2_new
        self.Cev_O2 = Cev_O2_new
        self.Cev_CO2 = Cev_CO2_new
        self.Csv_O2 = Csv_O2_new
        self.Csv_CO2 = Csv_CO2_new
        
        # 2. Thoracic venous mixing (A77-A78)
        Cv_O2_new, dCv_O2 = self.thoracicVenousO2(
            volumes['Vtv'], flows['Qhv'], flows['Qbv'], flows['Qamv'], 
            flows['Qrmv'], flows['Qev'], flows['Qsv'], dt
        )
        Cv_CO2_new, dCv_CO2 = self.thoracicVenousCO2(
            volumes['Vtv'], flows['Qhv'], flows['Qbv'], flows['Qamv'], 
            flows['Qrmv'], flows['Qev'], flows['Qsv'], dt
        )
        
        # Update mixed venous states
        self.Cv_O2 = Cv_O2_new
        self.Cv_CO2 = Cv_CO2_new
        
        # Package derivatives
        derivatives = {
            'dChv_O2': dChv_O2,
            'dChv_CO2': dChv_CO2,
            'dCbv_O2': dCbv_O2,
            'dCbv_CO2': dCbv_CO2,
            'dCamv_O2': dCamv_O2,
            'dCamv_CO2': dCamv_CO2,
            'dCrmv_O2': dCrmv_O2,
            'dCrmv_CO2': dCrmv_CO2,
            'dCev_O2': dCev_O2,
            'dCev_CO2': dCev_CO2,
            'dCsv_O2': dCsv_O2,
            'dCsv_CO2': dCsv_CO2,
            'dCv_O2': dCv_O2,
            'dCv_CO2': dCv_CO2
        }
        
        # Package outputs
        outputs = {
            'Chv_O2': self.Chv_O2,
            'Chv_CO2': self.Chv_CO2,
            'Cbv_O2': self.Cbv_O2,
            'Cbv_CO2': self.Cbv_CO2,
            'Camv_O2': self.Camv_O2,
            'Camv_CO2': self.Camv_CO2,
            'Crmv_O2': self.Crmv_O2,
            'Crmv_CO2': self.Crmv_CO2,
            'Cev_O2': self.Cev_O2,
            'Cev_CO2': self.Cev_CO2,
            'Csv_O2': self.Csv_O2,
            'Csv_CO2': self.Csv_CO2,
            'Cv_O2': self.Cv_O2,
            'Cv_CO2': self.Cv_CO2
        }
        
        return derivatives, outputs
