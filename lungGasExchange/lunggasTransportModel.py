import numpy as np


class LungGasTransferModel:
    """
    Lung Gas Transfer Model - Albanese 2016 Equations A42-A56

    Handles respiratory gas exchange including:
    - Dead space dynamics (A42-A43)
    - Alveolar gas balance (A44-A45)
    - Blood gas binding (A46-A49)
    - Pressure conversions (A50-A53)
    - Arterial mixing (A54-A56)
    """

    def __init__(self, params):
        """
        Initialize lung gas transfer model

        Parameters dict should contain:
        - Respiratory volumes: VD, VA, Vpp
        - Gas fractions: FI_O2, FI_CO2
        - Blood gas binding: Csat_O2, Csat_CO2, h1, h2, beta1, beta2, K1, K2, alpha1, alpha2
        - Environmental: Patm, Pws, Hgb
        - Gas exchange: K
        - Shunt: sh
        - Initial states: FD_O2_init, FD_CO2_init, FA_O2_init, FA_CO2_init
        """
        # Store parameters
        self.params = params

        # Respiratory volumes
        self.VD = params['VD']
        self.VA = params['VA']
        self.Vpp = params['Vpp']

        # Gas fractions (inspired air)
        self.FI_O2 = params['FI_O2']
        self.FI_CO2 = params['FI_CO2']

        # Blood gas binding parameters
        self.Csat_O2 = params['Csat_O2']
        self.Csat_CO2 = params['Csat_CO2']
        self.h1 = params['h1']
        self.h2 = params['h2']
        self.beta1 = params['beta1']
        self.beta2 = params['beta2']
        self.K1 = params['K1']
        self.K2 = params['K2']
        self.alpha1 = params['alpha1']
        self.alpha2 = params['alpha2']

        # Environmental
        self.Patm = params['Patm']
        self.Pws = params['Pws']
        self.Hgb = params['Hgb']

        # Conversion constant
        self.K = params['K']

        # Shunt fraction
        self.sh = params['sh']

        # Initialize state variables
        self.FD_O2 = params.get('FD_O2_init', 0.15)
        self.FD_CO2 = params.get('FD_CO2_init', 0.05)
        self.FA_O2 = params.get('FA_O2_init', 0.14)
        self.FA_CO2 = params.get('FA_CO2_init', 0.055)

    def deadSpaceO2(self, V_dot, VA_dot, phase, dt):
        """
        Dead space O2 balance (A42)

        Parameters:
        - V_dot: ventilation rate
        - VA_dot: alveolar ventilation rate
        - phase: respiratory phase (1=inspiration, 0=expiration)
        - dt: time step

        Returns:
        - dFD_O2: O2 fraction derivative
        - FD_O2_new: updated O2 fraction
        """
        if phase == 1:  # Inspiration
            term1 = V_dot * (self.FI_O2 - self.FD_O2)
            term2 = 0
        else:  # Expiration
            term1 = 0
            term2 = VA_dot * (self.FD_O2 - self.FA_O2)

        dFD_O2 = (term1 + term2) / self.VD
        FD_O2_new = self.FD_O2 + dFD_O2 * dt

        return dFD_O2, FD_O2_new

    def deadSpaceCO2(self, V_dot, VA_dot, phase, dt):
        """
        Dead space CO2 balance (A43)

        Parameters:
        - V_dot: ventilation rate
        - VA_dot: alveolar ventilation rate
        - phase: respiratory phase (1=inspiration, 0=expiration)
        - dt: time step

        Returns:
        - dFD_CO2: CO2 fraction derivative
        - FD_CO2_new: updated CO2 fraction
        """
        if phase == 1:  # Inspiration
            term1 = V_dot * (self.FI_CO2 - self.FD_CO2)
            term2 = 0
        else:  # Expiration
            term1 = 0
            term2 = VA_dot * (self.FD_CO2 - self.FA_CO2)

        dFD_CO2 = (term1 + term2) / self.VD
        FD_CO2_new = self.FD_CO2 + dFD_CO2 * dt

        return dFD_CO2, FD_CO2_new

    def alveolarO2(self, V_dot, VA_dot, Qpa, Cpp_O2, Cv_O2, dCpp_O2_dt, phase, dt):
        """
        Alveolar O2 balance (A44)

        Parameters:
        - V_dot: ventilation rate
        - VA_dot: alveolar ventilation rate
        - Qpa: pulmonary arterial flow
        - Cpp_O2: pulmonary capillary O2 content
        - Cv_O2: mixed venous O2 content
        - dCpp_O2_dt: time derivative of capillary O2
        - phase: respiratory phase
        - dt: time step

        Returns:
        - dFA_O2: O2 fraction derivative
        - FA_O2_new: updated O2 fraction
        """
        if phase == 1:  # Inspiration
            term1 = VA_dot * (self.FD_O2 - self.FA_O2)
        else:  # Expiration
            term1 = VA_dot * (self.FD_O2 - self.FA_O2)

        term2 = self.K * (Qpa * (1 - self.sh) * (Cpp_O2 - Cv_O2) + self.Vpp * dCpp_O2_dt)
        dFA_O2 = (term1 - term2) / self.VA
        FA_O2_new = self.FA_O2 + dFA_O2 * dt

        return dFA_O2, FA_O2_new

    def alveolarCO2(self, V_dot, VA_dot, Qpa, Cpp_CO2, Cv_CO2, dCpp_CO2_dt, phase, dt):
        """
        Alveolar CO2 balance (A45)

        Parameters:
        - V_dot: ventilation rate
        - VA_dot: alveolar ventilation rate
        - Qpa: pulmonary arterial flow
        - Cpp_CO2: pulmonary capillary CO2 content
        - Cv_CO2: mixed venous CO2 content
        - dCpp_CO2_dt: time derivative of capillary CO2
        - phase: respiratory phase
        - dt: time step

        Returns:
        - dFA_CO2: CO2 fraction derivative
        - FA_CO2_new: updated CO2 fraction
        """
        if phase == 1:  # Inspiration
            term1 = VA_dot * (self.FD_CO2 - self.FA_CO2)
        else:  # Expiration
            term1 = VA_dot * (self.FD_CO2 - self.FA_CO2)

        term2 = self.K * (Qpa * (1 - self.sh) * (Cpp_CO2 - Cv_CO2) + self.Vpp * dCpp_CO2_dt)
        dFA_CO2 = (term1 - term2) / self.VA
        FA_CO2_new = self.FA_CO2 + dFA_CO2 * dt

        return dFA_CO2, FA_CO2_new

    def o2Concentration(self, Xpp_O2):
        """
        O2 concentration (A46)

        Parameters:
        - Xpp_O2: O2 saturation variable

        Returns:
        - Cpp_O2: O2 concentration
        """
        Cpp_O2 = self.Csat_O2 * (Xpp_O2 ** (1 / self.h1)) / (1 + (Xpp_O2 ** (1 / self.h1)))
        return Cpp_O2

    def o2SaturationVariable(self, Ppp_O2, Ppp_CO2):
        """
        O2 saturation variable (A47)

        Parameters:
        - Ppp_O2: pulmonary capillary O2 pressure
        - Ppp_CO2: pulmonary capillary CO2 pressure

        Returns:
        - Xpp_O2: O2 saturation variable
        """
        Xpp_O2 = Ppp_O2 * (1 + self.beta1 * Ppp_CO2) / (self.K1 * (1 + self.alpha1 * Ppp_CO2))
        return Xpp_O2

    def co2Concentration(self, Xpp_CO2):
        """
        CO2 concentration (A48)

        Parameters:
        - Xpp_CO2: CO2 saturation variable

        Returns:
        - Cpp_CO2: CO2 concentration
        """
        Cpp_CO2 = self.Csat_CO2 * (Xpp_CO2 ** (1 / self.h2)) / (1 + (Xpp_CO2 ** (1 / self.h2)))
        return Cpp_CO2

    def co2SaturationVariable(self, Ppp_CO2, Ppp_O2):
        """
        CO2 saturation variable (A49)

        Parameters:
        - Ppp_CO2: pulmonary capillary CO2 pressure
        - Ppp_O2: pulmonary capillary O2 pressure

        Returns:
        - Xpp_CO2: CO2 saturation variable
        """
        Xpp_CO2 = Ppp_CO2 * (1 + self.beta2 * Ppp_O2) / (self.K2 * (1 + self.alpha2 * Ppp_O2))
        return Xpp_CO2

    def alveolarPressures(self):
        """
        Convert alveolar fractions to pressures (A52, A53)

        Returns:
        - PA_O2: alveolar O2 pressure
        - PA_CO2: alveolar CO2 pressure
        """
        PA_O2 = self.FA_O2 * (self.Patm - self.Pws)
        PA_CO2 = self.FA_CO2 * (self.Patm - self.Pws)
        return PA_O2, PA_CO2

    def equilibriumPressures(self, PA_O2, PA_CO2):
        """
        Equilibrium between alveoli and capillaries (A50, A51)

        Parameters:
        - PA_O2: alveolar O2 pressure
        - PA_CO2: alveolar CO2 pressure

        Returns:
        - Ppp_O2: capillary O2 pressure
        - Ppp_CO2: capillary CO2 pressure
        """
        Ppp_O2 = PA_O2
        Ppp_CO2 = PA_CO2
        return Ppp_O2, Ppp_CO2

    def arterialGasMixing(self, Qpp, Cpp_O2, Qps, Cv_O2):
        """
        Arterial O2 mixing - shunt + gas exchange (A54)

        Parameters:
        - Qpp: perfused capillary flow
        - Cpp_O2: capillary O2 content
        - Qps: shunt flow
        - Cv_O2: venous O2 content

        Returns:
        - Ca_O2: arterial O2 content
        """
        Ca_O2 = (Qpp * Cpp_O2 + Qps * Cv_O2) / (Qpp + Qps)
        return Ca_O2

    def arterialCO2Mixing(self, Qpp, Cpp_CO2, Qps, Cv_CO2):
        """
        Arterial CO2 mixing - shunt + gas exchange (A55)

        Parameters:
        - Qpp: perfused capillary flow
        - Cpp_CO2: capillary CO2 content
        - Qps: shunt flow
        - Cv_CO2: venous CO2 content

        Returns:
        - Ca_CO2: arterial CO2 content
        """
        Ca_CO2 = (Qpp * Cpp_CO2 + Qps * Cv_CO2) / (Qpp + Qps)
        return Ca_CO2

    def arterialO2Saturation(self, Ca_O2, Pa_O2):
        """
        Arterial O2 saturation percentage (A56)

        Parameters:
        - Ca_O2: arterial O2 content
        - Pa_O2: arterial O2 pressure

        Returns:
        - Sa_O2_percent: arterial O2 saturation (%)
        """
        Sa_O2_percent = ((Ca_O2 - Pa_O2 * 0.003 / 100) / (self.Hgb * 1.34)) * 100
        return Sa_O2_percent

    def compute_derivatives(self, Qpa, Cv_O2, Cv_CO2, V_dot, VA_dot, phase, dt):
        """
        Compute all lung gas transfer for one time step

        Parameters:
        - Qpa: pulmonary arterial flow (mL/s)
        - Cv_O2: mixed venous O2 content (mL/L)
        - Cv_CO2: mixed venous CO2 content (mL/L)
        - V_dot: ventilation rate (mL/s)
        - VA_dot: alveolar ventilation rate (mL/s)
        - phase: respiratory phase (1=inspiration, 0=expiration)
        - dt: time step (s)

        Returns:
        - derivatives: dict with all state derivatives
        - outputs: dict with computed pressures, concentrations, saturations
        """

        # 1. Dead Space Gas Balance (A42-A43)
        dFD_O2, FD_O2_new = self.deadSpaceO2(V_dot, VA_dot, phase, dt)
        dFD_CO2, FD_CO2_new = self.deadSpaceCO2(V_dot, VA_dot, phase, dt)

        # 2. Compute pulmonary capillary concentrations for alveolar equations
        # Using previous alveolar fractions to get pressures
        PA_O2_prev, PA_CO2_prev = self.alveolarPressures()
        Ppp_O2_prev, Ppp_CO2_prev = self.equilibriumPressures(PA_O2_prev, PA_CO2_prev)

        Xpp_O2_prev = self.o2SaturationVariable(Ppp_O2_prev, Ppp_CO2_prev)
        Cpp_O2_prev = self.o2Concentration(Xpp_O2_prev)

        Xpp_CO2_prev = self.co2SaturationVariable(Ppp_CO2_prev, Ppp_O2_prev)
        Cpp_CO2_prev = self.co2Concentration(Xpp_CO2_prev)

        # Approximate time derivatives (zero for simplicity - can be improved)
        dCpp_O2_dt = 0.0
        dCpp_CO2_dt = 0.0

        # 3. Alveolar Gas Balance (A44-A45)
        dFA_O2, FA_O2_new = self.alveolarO2(
            V_dot, VA_dot, Qpa, Cpp_O2_prev, Cv_O2, dCpp_O2_dt, phase, dt
        )
        dFA_CO2, FA_CO2_new = self.alveolarCO2(
            V_dot, VA_dot, Qpa, Cpp_CO2_prev, Cv_CO2, dCpp_CO2_dt, phase, dt
        )

        # Update state variables
        self.FD_O2 = FD_O2_new
        self.FD_CO2 = FD_CO2_new
        self.FA_O2 = FA_O2_new
        self.FA_CO2 = FA_CO2_new

        # 4. Convert alveolar fractions to pressures (A52-A53)
        PA_O2, PA_CO2 = self.alveolarPressures()

        # 5. Equilibrium pressures (A50-A51)
        Ppp_O2, Ppp_CO2 = self.equilibriumPressures(PA_O2, PA_CO2)

        # 6. Blood gas binding (A46-A49)
        Xpp_O2 = self.o2SaturationVariable(Ppp_O2, Ppp_CO2)
        Cpp_O2 = self.o2Concentration(Xpp_O2)

        Xpp_CO2 = self.co2SaturationVariable(Ppp_CO2, Ppp_O2)
        Cpp_CO2 = self.co2Concentration(Xpp_CO2)

        # 7. Arterial mixing with shunt (A54-A55)
        Qpp = Qpa * (1 - self.sh)  # Perfused capillary flow
        Qps = Qpa * self.sh  # Shunt flow

        Ca_O2 = self.arterialGasMixing(Qpp, Cpp_O2, Qps, Cv_O2)
        Ca_CO2 = self.arterialCO2Mixing(Qpp, Cpp_CO2, Qps, Cv_CO2)

        # 8. Arterial O2 saturation (A56)
        Pa_O2 = 100.0  # Placeholder - would need inverse calculation
        Sa_O2_percent = self.arterialO2Saturation(Ca_O2, Pa_O2)

        # Package derivatives
        derivatives = {
            'dFD_O2': dFD_O2,
            'dFD_CO2': dFD_CO2,
            'dFA_O2': dFA_O2,
            'dFA_CO2': dFA_CO2
        }

        # Package outputs
        outputs = {
            'FD_O2': self.FD_O2,
            'FD_CO2': self.FD_CO2,
            'FA_O2': self.FA_O2,
            'FA_CO2': self.FA_CO2,
            'PA_O2': PA_O2,
            'PA_CO2': PA_CO2,
            'Ppp_O2': Ppp_O2,
            'Ppp_CO2': Ppp_CO2,
            'Cpp_O2': Cpp_O2,
            'Cpp_CO2': Cpp_CO2,
            'Ca_O2': Ca_O2,
            'Ca_CO2': Ca_CO2,
            'Sa_O2_percent': Sa_O2_percent,
            'Qpp': Qpp,
            'Qps': Qps
        }

        return derivatives, outputs