def thoracicVenousO2(Vtv, Cv_O2_old, Qhv, Chv_O2, Qbv, Cbv_O2, Qamv, Camv_O2, Qrmv, Crmv_O2, Qev, Cev_O2, Qsv, Csv_O2, dt):
    """Thoracic venous O2 mixing (A77) - NOW 6 VENOUS BEDS"""
    dCv_O2 = (Qhv * (Chv_O2 - Cv_O2_old) + Qbv * (Cbv_O2 - Cv_O2_old) +
              Qamv * (Camv_O2 - Cv_O2_old) + Qrmv * (Crmv_O2 - Cv_O2_old) +  # ADDED RESTING MUSCLE
              Qev * (Cev_O2 - Cv_O2_old) + Qsv * (Csv_O2 - Cv_O2_old)) / Vtv
    Cv_O2_new = Cv_O2_old + dCv_O2 * dt
    return Cv_O2_new, dCv_O2

def thoracicVenousCO2(Vtv, Cv_CO2_old, Qhv, Chv_CO2, Qbv, Cbv_CO2, Qamv, Camv_CO2, Qrmv, Crmv_CO2, Qev, Cev_CO2, Qsv, Csv_CO2, dt):
    """Thoracic venous CO2 mixing (A78) - NOW 6 VENOUS BEDS"""
    dCv_CO2 = (Qhv * (Chv_CO2 - Cv_CO2_old) + Qbv * (Cbv_CO2 - Cv_CO2_old) +
               Qamv * (Camv_CO2 - Cv_CO2_old) + Qrmv * (Crmv_CO2 - Cv_CO2_old) +  # ADDED RESTING MUSCLE
               Qev * (Cev_CO2 - Cv_CO2_old) + Qsv * (Csv_CO2 - Cv_CO2_old)) / Vtv
    Cv_CO2_new = Cv_CO2_old + dCv_CO2 * dt
    return Cv_CO2_new, dCv_CO2