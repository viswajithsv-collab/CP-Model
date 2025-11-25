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

    States: Chv_O2, Chv_CO2, Cbv_O2, Cbv_CO2, Camv_O2, Camv_CO2,
            Crmv_O2, Crmv_CO2, Cev_O2, Cev_CO2, Csv_O2, Csv_CO2,
            Cv_O2, Cv_CO2 (14)
    """

    def __init__(self, params):
        """
        Initialize venous gas transport model

        Parameters dict should contain:
        (No state variables - all passed to compute_derivatives)
        """
        # Store parameters
        self.params = params

    def coronaryVenousO2(self, Chv_O2, Vhv, Qhp, Chp_O2):
        """
        Coronary venous O2 transport (A67)
        Vhv · dChv,O2/dt = Qhp · (Chp,O2 - Chv,O2)

        Parameters:
        - Chv_O2: coronary venous O2 concentration
        - Vhv: coronary venous volume
        - Qhp: coronary blood flow
        - Chp_O2: coronary tissue O2 concentration

        Returns:
        - dChv_O2: concentration derivative
        """
        dChv_O2 = Qhp * (Chp_O2 - Chv_O2) / Vhv
        return dChv_O2

    def coronaryVenousCO2(self, Chv_CO2, Vhv, Qhp, Chp_CO2):
        """
        Coronary venous CO2 transport (A68)
        Vhv · dChv,CO2/dt = Qhp · (Chp,CO2 - Chv,CO2)

        Parameters:
        - Chv_CO2: coronary venous CO2 concentration
        - Vhv: coronary venous volume
        - Qhp: coronary blood flow
        - Chp_CO2: coronary tissue CO2 concentration

        Returns:
        - dChv_CO2: concentration derivative
        """
        dChv_CO2 = Qhp * (Chp_CO2 - Chv_CO2) / Vhv
        return dChv_CO2

    def brainVenousO2(self, Cbv_O2, Vbv, Qbp, Cbp_O2):
        """
        Brain venous O2 transport (A69)
        Vbv · dCbv,O2/dt = Qbp · (Cbp,O2 - Cbv,O2)

        Parameters:
        - Cbv_O2: brain venous O2 concentration
        - Vbv: brain venous volume
        - Qbp: brain blood flow
        - Cbp_O2: brain tissue O2 concentration

        Returns:
        - dCbv_O2: concentration derivative
        """
        dCbv_O2 = Qbp * (Cbp_O2 - Cbv_O2) / Vbv
        return dCbv_O2

    def brainVenousCO2(self, Cbv_CO2, Vbv, Qbp, Cbp_CO2):
        """
        Brain venous CO2 transport (A70)
        Vbv · dCbv,CO2/dt = Qbp · (Cbp,CO2 - Cbv,CO2)

        Parameters:
        - Cbv_CO2: brain venous CO2 concentration
        - Vbv: brain venous volume
        - Qbp: brain blood flow
        - Cbp_CO2: brain tissue CO2 concentration

        Returns:
        - dCbv_CO2: concentration derivative
        """
        dCbv_CO2 = Qbp * (Cbp_CO2 - Cbv_CO2) / Vbv
        return dCbv_CO2

    def activeMuscleVenousO2(self, Camv_O2, Vamv, Qamp, Camp_O2):
        """
        Active muscle venous O2 transport (A71)
        Vamv · dCamv,O2/dt = Qamp · (Camp,O2 - Camv,O2)

        Parameters:
        - Camv_O2: active muscle venous O2 concentration
        - Vamv: active muscle venous volume
        - Qamp: active muscle blood flow
        - Camp_O2: active muscle tissue O2 concentration

        Returns:
        - dCamv_O2: concentration derivative
        """
        dCamv_O2 = Qamp * (Camp_O2 - Camv_O2) / Vamv
        return dCamv_O2

    def activeMuscleVenousCO2(self, Camv_CO2, Vamv, Qamp, Camp_CO2):
        """
        Active muscle venous CO2 transport (A72)
        Vamv · dCamv,CO2/dt = Qamp · (Camp,CO2 - Camv,CO2)

        Parameters:
        - Camv_CO2: active muscle venous CO2 concentration
        - Vamv: active muscle venous volume
        - Qamp: active muscle blood flow
        - Camp_CO2: active muscle tissue CO2 concentration

        Returns:
        - dCamv_CO2: concentration derivative
        """
        dCamv_CO2 = Qamp * (Camp_CO2 - Camv_CO2) / Vamv
        return dCamv_CO2

    def restingMuscleVenousO2(self, Crmv_O2, Vrmv, Qrmp, Crmp_O2):
        """
        Resting muscle venous O2 transport (A71 variant)
        Vrmv · dCrmv,O2/dt = Qrmp · (Crmp,O2 - Crmv,O2)

        Parameters:
        - Crmv_O2: resting muscle venous O2 concentration
        - Vrmv: resting muscle venous volume
        - Qrmp: resting muscle blood flow
        - Crmp_O2: resting muscle tissue O2 concentration

        Returns:
        - dCrmv_O2: concentration derivative
        """
        dCrmv_O2 = Qrmp * (Crmp_O2 - Crmv_O2) / Vrmv
        return dCrmv_O2

    def restingMuscleVenousCO2(self, Crmv_CO2, Vrmv, Qrmp, Crmp_CO2):
        """
        Resting muscle venous CO2 transport (A72 variant)
        Vrmv · dCrmv,CO2/dt = Qrmp · (Crmp,CO2 - Crmv,CO2)

        Parameters:
        - Crmv_CO2: resting muscle venous CO2 concentration
        - Vrmv: resting muscle venous volume
        - Qrmp: resting muscle blood flow
        - Crmp_CO2: resting muscle tissue CO2 concentration

        Returns:
        - dCrmv_CO2: concentration derivative
        """
        dCrmv_CO2 = Qrmp * (Crmp_CO2 - Crmv_CO2) / Vrmv
        return dCrmv_CO2

    def extrasplanchnicVenousO2(self, Cev_O2, Vev, Qep, Cep_O2):
        """
        Extrasplanchnic venous O2 transport (A73)
        Vev · dCev,O2/dt = Qep · (Cep,O2 - Cev,O2)

        Parameters:
        - Cev_O2: extrasplanchnic venous O2 concentration
        - Vev: extrasplanchnic venous volume
        - Qep: extrasplanchnic blood flow
        - Cep_O2: extrasplanchnic tissue O2 concentration

        Returns:
        - dCev_O2: concentration derivative
        """
        dCev_O2 = Qep * (Cep_O2 - Cev_O2) / Vev
        return dCev_O2

    def extrasplanchnicVenousCO2(self, Cev_CO2, Vev, Qep, Cep_CO2):
        """
        Extrasplanchnic venous CO2 transport (A74)
        Vev · dCev,CO2/dt = Qep · (Cep,CO2 - Cev,CO2)

        Parameters:
        - Cev_CO2: extrasplanchnic venous CO2 concentration
        - Vev: extrasplanchnic venous volume
        - Qep: extrasplanchnic blood flow
        - Cep_CO2: extrasplanchnic tissue CO2 concentration

        Returns:
        - dCev_CO2: concentration derivative
        """
        dCev_CO2 = Qep * (Cep_CO2 - Cev_CO2) / Vev
        return dCev_CO2

    def splanchnicVenousO2(self, Csv_O2, Vsv, Qsp, Csp_O2):
        """
        Splanchnic venous O2 transport (A75)
        Vsv · dCsv,O2/dt = Qsp · (Csp,O2 - Csv,O2)

        Parameters:
        - Csv_O2: splanchnic venous O2 concentration
        - Vsv: splanchnic venous volume
        - Qsp: splanchnic blood flow
        - Csp_O2: splanchnic tissue O2 concentration

        Returns:
        - dCsv_O2: concentration derivative
        """
        dCsv_O2 = Qsp * (Csp_O2 - Csv_O2) / Vsv
        return dCsv_O2

    def splanchnicVenousCO2(self, Csv_CO2, Vsv, Qsp, Csp_CO2):
        """
        Splanchnic venous CO2 transport (A76)
        Vsv · dCsv,CO2/dt = Qsp · (Csp,CO2 - Csv,CO2)

        Parameters:
        - Csv_CO2: splanchnic venous CO2 concentration
        - Vsv: splanchnic venous volume
        - Qsp: splanchnic blood flow
        - Csp_CO2: splanchnic tissue CO2 concentration

        Returns:
        - dCsv_CO2: concentration derivative
        """
        dCsv_CO2 = Qsp * (Csp_CO2 - Csv_CO2) / Vsv
        return dCsv_CO2

    def thoracicVenousO2(self, Cv_O2, Chv_O2, Cbv_O2, Camv_O2, Crmv_O2, Cev_O2, Csv_O2,
                         Vtv, Qhv, Qbv, Qamv, Qrmv, Qev, Qsv):
        """
        Thoracic venous O2 mixing (A77) - ALL 6 VENOUS BEDS

        Vtv · dCv,O2/dt = Qhv·(Chv,O2 - Cv,O2) + Qbv·(Cbv,O2 - Cv,O2)
                         + Qamv·(Camv,O2 - Cv,O2) + Qrmv·(Crmv,O2 - Cv,O2)
                         + Qev·(Cev,O2 - Cv,O2) + Qsv·(Csv,O2 - Cv,O2)

        Parameters:
        - Cv_O2: mixed venous O2 concentration
        - Chv_O2, Cbv_O2, Camv_O2, Crmv_O2, Cev_O2, Csv_O2: venous bed concentrations
        - Vtv: thoracic venous volume
        - Qhv, Qbv, Qamv, Qrmv, Qev, Qsv: venous flows from all 6 beds

        Returns:
        - dCv_O2: concentration derivative
        """
        dCv_O2 = (Qhv * (Chv_O2 - Cv_O2) +
                  Qbv * (Cbv_O2 - Cv_O2) +
                  Qamv * (Camv_O2 - Cv_O2) +
                  Qrmv * (Crmv_O2 - Cv_O2) +
                  Qev * (Cev_O2 - Cv_O2) +
                  Qsv * (Csv_O2 - Cv_O2)) / Vtv

        return dCv_O2

    def thoracicVenousCO2(self, Cv_CO2, Chv_CO2, Cbv_CO2, Camv_CO2, Crmv_CO2, Cev_CO2, Csv_CO2,
                          Vtv, Qhv, Qbv, Qamv, Qrmv, Qev, Qsv):
        """
        Thoracic venous CO2 mixing (A78) - ALL 6 VENOUS BEDS

        Vtv · dCv,CO2/dt = Qhv·(Chv,CO2 - Cv,CO2) + Qbv·(Cbv,CO2 - Cv,CO2)
                          + Qamv·(Camv,CO2 - Cv,CO2) + Qrmv·(Crmv,CO2 - Cv,CO2)
                          + Qev·(Cev,CO2 - Cv,CO2) + Qsv·(Csv,CO2 - Cv,CO2)

        Parameters:
        - Cv_CO2: mixed venous CO2 concentration
        - Chv_CO2, Cbv_CO2, Camv_CO2, Crmv_CO2, Cev_CO2, Csv_CO2: venous bed concentrations
        - Vtv: thoracic venous volume
        - Qhv, Qbv, Qamv, Qrmv, Qev, Qsv: venous flows from all 6 beds

        Returns:
        - dCv_CO2: concentration derivative
        """
        dCv_CO2 = (Qhv * (Chv_CO2 - Cv_CO2) +
                   Qbv * (Cbv_CO2 - Cv_CO2) +
                   Qamv * (Camv_CO2 - Cv_CO2) +
                   Qrmv * (Crmv_CO2 - Cv_CO2) +
                   Qev * (Cev_CO2 - Cv_CO2) +
                   Qsv * (Csv_CO2 - Cv_CO2)) / Vtv

        return dCv_CO2

    def compute_derivatives(self, t, Chv_O2, Chv_CO2, Cbv_O2, Cbv_CO2, Camv_O2, Camv_CO2,
                            Crmv_O2, Crmv_CO2, Cev_O2, Cev_CO2, Csv_O2, Csv_CO2,
                            Cv_O2, Cv_CO2,
                            Vhv, Vbv, Vamv, Vrmv, Vev, Vsv, Vtv,
                            Qhp, Qbp, Qamp, Qrmp, Qep, Qsp,
                            Qhv, Qbv, Qamv, Qrmv, Qev, Qsv,
                            Chp_O2, Chp_CO2, Cbp_O2, Cbp_CO2, Camp_O2, Camp_CO2,
                            Crmp_O2, Crmp_CO2, Cep_O2, Cep_CO2, Csp_O2, Csp_CO2):
        """
        Compute all venous gas transport derivatives for Euler integration

        State variables (passed in):
        - Chv_O2, Chv_CO2: coronary venous concentrations
        - Cbv_O2, Cbv_CO2: brain venous concentrations
        - Camv_O2, Camv_CO2: active muscle venous concentrations
        - Crmv_O2, Crmv_CO2: resting muscle venous concentrations
        - Cev_O2, Cev_CO2: extrasplanchnic venous concentrations
        - Csv_O2, Csv_CO2: splanchnic venous concentrations
        - Cv_O2, Cv_CO2: mixed venous (thoracic) concentrations

        Coupling inputs (from SystemicModel):
        - Vhv, Vbv, Vamv, Vrmv, Vev, Vsv, Vtv: venous volumes
        - Qhp, Qbp, Qamp, Qrmp, Qep, Qsp: peripheral flows
        - Qhv, Qbv, Qamv, Qrmv, Qev, Qsv: venous flows

        Coupling inputs (from TissueGasExchangeModel):
        - Chp_O2, Chp_CO2, Cbp_O2, Cbp_CO2, etc.: tissue concentrations

        Returns:
        - derivatives: dict with all concentration derivatives
        - outputs: dict with concentrations
        """

        # 1. Individual venous beds (A67-A76)
        dChv_O2 = self.coronaryVenousO2(Chv_O2, Vhv, Qhp, Chp_O2)
        dChv_CO2 = self.coronaryVenousCO2(Chv_CO2, Vhv, Qhp, Chp_CO2)

        dCbv_O2 = self.brainVenousO2(Cbv_O2, Vbv, Qbp, Cbp_O2)
        dCbv_CO2 = self.brainVenousCO2(Cbv_CO2, Vbv, Qbp, Cbp_CO2)

        dCamv_O2 = self.activeMuscleVenousO2(Camv_O2, Vamv, Qamp, Camp_O2)
        dCamv_CO2 = self.activeMuscleVenousCO2(Camv_CO2, Vamv, Qamp, Camp_CO2)

        dCrmv_O2 = self.restingMuscleVenousO2(Crmv_O2, Vrmv, Qrmp, Crmp_O2)
        dCrmv_CO2 = self.restingMuscleVenousCO2(Crmv_CO2, Vrmv, Qrmp, Crmp_CO2)

        dCev_O2 = self.extrasplanchnicVenousO2(Cev_O2, Vev, Qep, Cep_O2)
        dCev_CO2 = self.extrasplanchnicVenousCO2(Cev_CO2, Vev, Qep, Cep_CO2)

        dCsv_O2 = self.splanchnicVenousO2(Csv_O2, Vsv, Qsp, Csp_O2)
        dCsv_CO2 = self.splanchnicVenousCO2(Csv_CO2, Vsv, Qsp, Csp_CO2)

        # 2. Thoracic venous mixing (A77-A78)
        dCv_O2 = self.thoracicVenousO2(Cv_O2, Chv_O2, Cbv_O2, Camv_O2, Crmv_O2, Cev_O2, Csv_O2,
                                       Vtv, Qhv, Qbv, Qamv, Qrmv, Qev, Qsv)
        dCv_CO2 = self.thoracicVenousCO2(Cv_CO2, Chv_CO2, Cbv_CO2, Camv_CO2, Crmv_CO2, Cev_CO2, Csv_CO2,
                                         Vtv, Qhv, Qbv, Qamv, Qrmv, Qev, Qsv)

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
            'Chv_O2': Chv_O2,
            'Chv_CO2': Chv_CO2,
            'Cbv_O2': Cbv_O2,
            'Cbv_CO2': Cbv_CO2,
            'Camv_O2': Camv_O2,
            'Camv_CO2': Camv_CO2,
            'Crmv_O2': Crmv_O2,
            'Crmv_CO2': Crmv_CO2,
            'Cev_O2': Cev_O2,
            'Cev_CO2': Cev_CO2,
            'Csv_O2': Csv_O2,
            'Csv_CO2': Csv_CO2,
            'Cv_O2': Cv_O2,
            'Cv_CO2': Cv_CO2
        }

        return derivatives, outputs