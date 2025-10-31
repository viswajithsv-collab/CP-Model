%%This file contains all the functions and essential codes
%%to run the model in full. Use this file to simulate / run the model in
%%the absense of Baroreflex Regulation.

%%The next three lines call three files contained in the folder that
%%initialize all the constants of the model and the variables used in this
%%code. 

%% (C) Viswajith S Vasudevan, BME, Cornell
Constants;
HeartVariables;
Initialize_HW;

%Set Heart Rate (HR)
HR = 75;
%Total time for simulation.
t = 0:0.001:40;
h = 0.001; %step size for simulation.
%Double-Hill Function
alpha = [0.103,0.408];
n = [1.9,21.9];
E = phi1(t,HR,alpha,n);

Emaxlv = 2.4;  %Use Emaxlv = 1.2 for unhealthy in Part A Scenario 2
Emaxrv = 1.8;

for i = 1:length(t)-1
%----------------------------Heart------------------------------------------
    %Left Atrium
    dPla(i) = leftAtrium(Ppv(i),Pla(i),Rpv,Qmv(i),Cla);
    Pla(i+1) = Pla(i) + dPla(i)*h;

    %Right Atrium
    dPra(i) = rightAtrium(Pev(i),Pbv(i),Pra(i),Rdv+Rev+Rmv,Rbv+Rhv,Qtv(i),Cra);
    Pra(i+1) = Pra(i) + dPra(i)*h;

    %Left Ventricle
    [Vlv(i+1),Plv(i+1),Plvmax(i+1),Rlv(i+1)] = ventricle(Emaxlv,E(i),Vlv(i),Vulv,Qmv(i),Qao(i),krlv,kelv,P0lv,h);

    %Right Ventricle
    [Vrv(i+1),Prv(i+1),Prvmax(i+1),Rrv(i+1)] = ventricle(Emaxrv,E(i),Vrv(i),Vurv,Qtv(i),Qpu(i),krrv,kerv,P0rv,h);

%--------------------------------------------------------------------------

%---------------------Systemic Circulation---------------------------------
    %Systemic Artery
    dPsa(i) = systemicArtery(Qao(i),Psa(i),Psp(i),Rsa,Csa);
    Psa(i+1) = Psa(i)+ dPsa(i)*h;
    %Systemic Vascular Bed
    dPsp(i) = systemicVascular(Psp(i), Psa(i), Pdv(i), Pev(i), Pmv(i), Pbv(i), Phv(i), Rsa, Rdvb, Revb, Rmvb, Rbvb, Rhvb, Csvb, Cevb, Cmvb, Cbvb, Chvb);
    Psp(i+1) = Psp(i)+dPsp(i)*h;
    
    %Systemic Veins
    %Digestive Veins
   
    dPdv(i) = splanchicVenous(Psp(i),Pdv(i),Pra(i),0,Rdvb,Rdv,Csv);
    Pdv(i+1) = Pdv(i) + dPdv(i)*h;
    
    %Skeletal Muscles Veins
    %dPmv = skeletalmuscleVeins(Psvb(i),Pmv(i),Pra(i),dVumv(i),Rmp,Rmv,Cmv);
    dPmv(i) = skeletalmuscleVeins(Psp(i),Pmv(i),Pra(i),0,Rmvb,Rsmv,Cmv);
    Pmv(i+1) = Pmv(i) + dPmv(i)*h;
    
    %Brain Veins
    dPbv(i) = brainVeins(Psp(i),Pbv(i),Pra(i),Rbvb,Rbv,Cbv);
    Pbv(i+1) = Pbv(i) + dPbv(i)*h;
    
    %Coronary Veins
    dPhv(i) = coronaryVeins(Psp(i),Phv(i),Pra(i),Rhvb,Rhv,Chv);
    Phv(i+1) = Phv(i) + dPhv(i)*h;

   
%---------------------------------------------------------------------------

%---------------------Pulmonary Circulation---------------------------------
    %Pulmonary Artery
    dPpa = pulmonaryArtery(Qpu(i),Ppa(i),Ppp(i),Rpa,Cpa);
    Ppa(i+1) = Ppa(i)+dPpa*h;
    %Pulmonary Vascular bed
    dPpp = pulmonaryVascular(Ppa(i),Ppp(i),Ppv(i),Rpa,Rpvb,Cpvb);
    Ppp(i+1) = Ppp(i)+dPpp*h;
    %Pulmonary Veins
    dPpv = pulmonaryVeins(Ppp(i),Ppv(i),Pla(i),Rpvb,Rpv,Cpv);
    Ppv(i+1) = Ppv(i)+dPpv*h;
%---------------------------------------------------------------------------

 %Unstressed Volume
    Vu = Vusa + Vudp + Vuep + Vump + Vubp + Vuhp + Vudv + Vuev + Vumv + Vubv + Vuhv + Vura + Vupa + Vupvb + Vupv + Vula;

    %EOther Venous Circulation
    Vnet(i+1) = Csa*Psa(i+1) + (Csvb+Cevb+Cmvb+Cbvb+Chvb)*Psp(i+1) + Csv*Pdv(i+1) + Cmv*Pmv(i+1) + Cbv*Pbv(i+1) + Chv*Phv(i+1) + Cra*Pra(i+1) + Vrv(i+1) + Cpa*Ppa(i+1) + Cpvb*Ppp(i+1) + Cpv*Ppv(i+1) + Cla*Pla(i+1) + Vlv(i+1) + Vu;
    Pev(i+1) = extrasplanchicVenous(TBV, Vnet(i+1), Cev);

%Valves
    Qmv(i+1) = valves(Pla(i+1),Plv(i+1),Rla+Rmv);
    Qao(i+1) = valves(Plvmax(i+1),Psa(i+1),Rlv(i+1)+Raov);
    Qtv(i+1) = valves(Pra(i+1),Prv(i+1),Rra+Rtv);
    Qpu(i+1) = valves(Prvmax(i+1),Ppa(i+1),Rrv(i+1)+Rpulv);
end

%---------------------------------------------------------------------------

%---Part A Scenario 1-------------------------------------
LVEDV = max(Vlv(end-8001:end));
LVESV = min(Vlv(end-8001:end));
SV = LVEDV - LVESV;
CO = SV*HR/1000;
pulp = max(Pbv(end-8001:end))-min(Pbv(end-8001:end));

VariableNames = {'LVEDV'; 'LVESV'; 'SV'; 'CO';'PP_UB'};
Values = [LVEDV; LVESV; SV; CO; pulp];
Units = {'mL'; 'mL'; 'mL'; 'L/min'; 'mmHg'};

results = table(Values, Units, 'RowNames', VariableNames)

%---Part A Scenario 2--------------------------------------
SBP = max(Psa(end-8001:end));
DBP = min(Psa(end-8001:end));
EF = SV*100/LVEDV;

VariableNames2 = {'SBP';'DBP';'CO';'EF'};
Values2 = [SBP;DBP;CO;EF];
Units2 = {'mmHg';'mmHg';'L/min';'%'};

results2 = table(Values2,Units2,'RowNames',VariableNames2)

%---Part A Scenario 3------------------------------------
% Use CO from above and plot R_SA vs CO

%---Part A Scenario 4------------------------------------
% Set in Constants file Vudv as 121 and Vuev = 50. Now increase
% either one to see where Pdv falls below 8mmHg.
plot(t,Pdv)

