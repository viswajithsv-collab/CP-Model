%================Variables Explained==============================
% Pressures
% Psa - Systemic Arterial Pressure
% Plbp - Lower Body Peripheral Pressure (Originally Splanchnic Peripheral)
% Plbv - Lower Body Venous Pressure (Orignally Splanchnic Venous)
% Pubv - Upper Body Venous Pressure (Originally Extrasplanchnic Venous)
% Rsa - Systemic Arterial Resistance
% Rlbp - Lower Body Peripheral Resistance (Originally Splanchnic Peripheral
% Compliance)
% Rubp - Upper Body Peripheral Resistance (Originally Extrasplanchnic
% Peripheral Resistance)
% Clbp - Lower Body Peripheral Compliance (Originally Splanchnic Peripheral
% Compliance)
% Cubp - Upper Body Peripheral Compliance (Originally Extrasplanchnic
% Peripheral Compliance)
function dPlbp = systemicPeripheralRC(Psa,Plbp,Plbv,Pubv,Rsa,Rlbp,Rubp,Clbp,Cubp)
    f1 = (Plbp - Plbv)/Rlbp;
    f2 = (Plbp - Pubv)/Rubp;
    Fout = f1 + f2;
    Fin = (Psa - Plbp)/Rsa;
    dPlbp = (Fin - Fout)/(Clbp + Cubp);
end