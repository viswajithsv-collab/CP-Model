import numpy as np


class PulmonaryModel:
    """
    Pulmonary Circulation Model - Albanese 2016 Equations A18-A29

    Integrates:
    - Pulmonary artery (A18-A20)
    - Pulmonary vascular bed - peripheral + shunt (A21-A26)
    - Pulmonary veins (A27-A29)
    - Optional intrathoracic pressure effects for exercise
    """

    def __init__(self, params):
        """
        Initialize pulmonary model with parameters

        Parameters dict should contain:
        - Resistances: Rpa, Rpp, Rps, Rpv
        - Compliances: Cpa, Cpp, Cps, Cpv
        - Unstressed volumes: Vu_pa, Vu_pp, Vu_ps, Vu_pv
        - Initial states: Ppa_init, Ppvb_init, Ppv_init
        - Optional: P_thor (intrathoracic pressure for exercise)
        """
        # Store parameters
        self.params = params

        # Resistances
        self.Rpa = params['Rpa']  # Pulmonary artery
        self.Rpp = params['Rpp']  # Peripheral (gas exchange)
        self.Rps = params['Rps']  # Shunt (bypasses gas exchange)
        self.Rpv = params['Rpv']  # Pulmonary veins

        # Compliances
        self.Cpa = params['Cpa']  # Pulmonary artery
        self.Cpp = params['Cpp']  # Peripheral
        self.Cps = params['Cps']  # Shunt
        self.Cpv = params['Cpv']  # Pulmonary veins

        # Unstressed volumes
        self.Vu_pa = params['Vu_pa']
        self.Vu_pp = params['Vu_pp']
        self.Vu_ps = params['Vu_ps']
        self.Vu_pv = params['Vu_pv']

        # Initialize state variables
        self.Ppa = params.get('Ppa_init', 15.0)  # Pulmonary arterial pressure
        self.Ppvb = params.get('Ppvb_init', 12.0)  # Pulmonary vascular bed pressure
        self.Ppv = params.get('Ppv_init', 8.0)  # Pulmonary venous pressure

        # Intrathoracic pressure (for exercise - defaults to 0)
        self.P_thor = 0.0
        self.dP_thor = 0.0

    def pulmonaryArtery(self, Qin):
        """
        Pulmonary artery with optional intrathoracic pressure reference (A18-A20)

        A18: Cpa * d(Ppa - P_thor)/dt = Qrv,o - Qpa
        A19: Qpa = (Ppa - Ppp)/Rpa
        A20: Vpa = Cpa * (Ppa - P_thor) + Vu,pa

        Parameters:
        - Qin: inflow from right ventricle (pulmonary valve)

        Returns:
        - dPpa: pressure derivative
        - Qpa: outflow to pulmonary vascular bed
        - Vpa: volume
        """
        # A19: Outflow to pulmonary vascular bed
        Qpa = (self.Ppa - self.Ppvb) / self.Rpa

        # A18: Pressure derivative with intrathoracic reference
        dPpa = (Qin - Qpa) / self.Cpa + self.dP_thor

        # A20: Volume with intrathoracic reference
        Vpa = self.Cpa * (self.Ppa - self.P_thor) + self.Vu_pa

        return dPpa, Qpa, Vpa

    def pulmonaryVascular(self):
        """
        Pulmonary vascular bed with peripheral + shunt pathways (A21-A26)

        A21: (Cpp + Cps) * d(Ppvb - P_thor)/dt = Qpa - Qpp - Qps
        A22: Qpp = (Ppvb - Ppv)/Rpp (peripheral - gas exchange)
        A23: Qps = (Ppvb - Ppv)/Rps (shunt - bypasses gas exchange)
        A24: Ppvb = Ppp (pressure equivalence)
        A25: Vpp = Cpp * (Ppvb - P_thor) + Vu,pp
        A26: Vps = Cps * (Ppvb - P_thor) + Vu,ps

        Returns:
        - dPpvb: vascular bed pressure derivative
        - Qpp: peripheral flow (gas exchange)
        - Qps: shunt flow
        - Vpp: peripheral volume
        - Vps: shunt volume
        """
        # Inflow from pulmonary arteries
        Fin = (self.Ppa - self.Ppvb) / self.Rpa

        # A22: Peripheral flow (gas exchange path)
        Qpp = (self.Ppvb - self.Ppv) / self.Rpp

        # A23: Shunt flow (bypasses gas exchange)
        Qps = (self.Ppvb - self.Ppv) / self.Rps

        # A21: Pressure derivative with intrathoracic reference
        Ctotal = self.Cpp + self.Cps
        dPpvb = (Fin - Qpp - Qps) / Ctotal + self.dP_thor

        # A25: Peripheral volume
        Vpp = self.Cpp * (self.Ppvb - self.P_thor) + self.Vu_pp

        # A26: Shunt volume
        Vps = self.Cps * (self.Ppvb - self.P_thor) + self.Vu_ps

        return dPpvb, Qpp, Qps, Vpp, Vps

    def pulmonaryVeins(self, Qpp, Qps, Pla):
        """
        Pulmonary veins with optional intrathoracic pressure reference (A27-A29)

        A27: Cpv * d(Ppv - P_thor)/dt = Qpp + Qps - Qpv
        A28: Qpv = (Ppv - Pla)/Rpv
        A29: Vpv = Cpv * (Ppv - P_thor) + Vu,pv

        Parameters:
        - Qpp: peripheral inflow (from gas exchange)
        - Qps: shunt inflow
        - Pla: left atrial pressure

        Returns:
        - dPpv: pressure derivative
        - Qpv: outflow to left atrium
        - Vpv: volume
        """
        # A27: Total inflow (peripheral + shunt)
        Fin = Qpp + Qps

        # A28: Outflow to left atrium
        Qpv = (self.Ppv - Pla) / self.Rpv

        # A27: Pressure derivative with intrathoracic reference
        dPpv = (Fin - Qpv) / self.Cpv + self.dP_thor

        # A29: Volume with intrathoracic reference
        Vpv = self.Cpv * (self.Ppv - self.P_thor) + self.Vu_pv

        return dPpv, Qpv, Vpv

    def set_intrathoracic_pressure(self, P_thor, dP_thor):
        """
        Set intrathoracic pressure for exercise simulations

        Parameters:
        - P_thor: intrathoracic pressure (mmHg)
        - dP_thor: intrathoracic pressure derivative (mmHg/s)
        """
        self.P_thor = P_thor
        self.dP_thor = dP_thor

    def compute_derivatives(self, Qin, Pla):
        """
        Compute all pulmonary derivatives for one time step

        Parameters:
        - Qin: inflow from right ventricle (pulmonary valve)
        - Pla: left atrial pressure (from heart model)

        Returns:
        - derivatives: dict with all state derivatives
        - outputs: dict with computed flows and volumes
        """

        # 1. Pulmonary artery (A18-A20)
        dPpa, Qpa, Vpa = self.pulmonaryArtery(Qin)

        # 2. Pulmonary vascular bed (A21-A26)
        dPpvb, Qpp, Qps, Vpp, Vps = self.pulmonaryVascular()

        # 3. Pulmonary veins (A27-A29)
        dPpv, Qpv, Vpv = self.pulmonaryVeins(Qpp, Qps, Pla)

        # Package derivatives
        derivatives = {
            'dPpa': dPpa,
            'dPpvb': dPpvb,
            'dPpv': dPpv
        }

        # Package outputs
        outputs = {
            'Ppa': self.Ppa,
            'Ppvb': self.Ppvb,
            'Ppv': self.Ppv,
            'Qpa': Qpa,
            'Qpp': Qpp,
            'Qps': Qps,
            'Qpv': Qpv,
            'Vpa': Vpa,
            'Vpp': Vpp,
            'Vps': Vps,
            'Vpv': Vpv
        }

        return derivatives, outputs