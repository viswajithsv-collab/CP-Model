clc;
clear all;
Constants;
HeartVariables;
Initialize;
HR = 75;
t = 0:0.0001:16;
h = 0.0001;
%Double-Hill Function
alpha = [0.103,0.408];
n = [1.9,21.9];
E = phi1(t,HR,alpha,n);

Emaxlv = 2.7;
Eminlv = 0.06;
Emaxrv = 1.6;
Eminrv = 0.08;

for i = 1:length(t)-1
    %Left Atrium
    dPla = leftAtrium(Ppv(i),LAP(i),Rpv,Qmv(i),Cla);
    LAP(i+1) = LAP(i) + dPla*h;

    %Right Atrium
    dPra = rightAtrium(Plbv(i),Pubv(i),RAP(i),Rlbv,Rubv,Qtv(i),Cra);
    RAP(i+1) = RAP(i) + dPra*h;

    %Left Ventricle
    [LVV(i+1),LVP(i+1)] = ventricle1(Emaxlv,Eminlv,E(i),LVV(i),Vulv,Qmv(i),Qaov(i),h);

    %Right Ventricle
    [RVV(i+1),RVP(i+1)] = ventricle1(Emaxrv,Eminrv,E(i),RVV(i),Vurv,Qtv(i),Qpulv(i),h);

    %Systemic Artery Circulation
    dPsa = systemicArteryRC(Qaov(i),Psa(i),Plbp(i),Rsa,Csa);
    Psa(i+1) = Psa(i)+dPsa*h;

    % Lower Body (originally Splanchnic) Peripheral Circulation
    dPlbp = systemicPeripheralRC(Psa(i),Plbp(i),Plbv(i),Pubv(i),Rsa,Rlbp,Rubp,Clbp,Cubp);
    Plbp(i+1) = Plbp(i)+dPlbp*h;

    %dPev = extrasplanchicVenous(Psp(i),Pev(i),RAP(i),dVuev(i),Rep,Rev,Cev);
    dPubv = extrasplanchicVenous(Plbp(i),Pubv(i),RAP(i),0,Rubp,Rubv,Cubv);
    Pubv(i+1) = Pubv(i)+dPubv*h;

    %Pulmonary Circulation
    dPpa = pulmonaryArteryRC(Qpulv(i),Ppa(i),Ppp(i),Rpa,Cpa); %RC(Fin,Ppa,Ppp,Rpa,Cpa)
    Ppa(i+1) = Ppa(i)+dPpa*h;
    dPpp = pulmonaryPeripheralRC(Ppa(i),Ppp(i),Ppv(i),Rpa,Rpp,Cpp);
    Ppp(i+1) = Ppp(i)+dPpp*h;
    dPpv = pulmonaryVeins(Ppp(i),Ppv(i),LAP(i),Rpp,Rpv,Cpv);
    Ppv(i+1) = Ppv(i)+dPpv*h;

    %Unstressed Volume
    %Vu(i+1) = Vusa + Vusp + Vuep + Vusv(i+1) + Vuev(i+1) + Vura + Vupa + Vupp + Vupv + Vula;
    Vu(i+1) = Vusa + Vulbp + Vuubp + Vulbv + Vuubv + Vura + Vupa + Vupp + Vupv + Vula;
    %dVuev(i+1) = (Vuev(i+1) - Vuev(i))/h;

    %Splanchic Venous Circulation
    Vlbv(i+1) = Csa*Psa(i+1) + (Clbp+Cubp)*Plbp(i+1) + Cubv*Pubv(i+1) + Cra*RAP(i+1) + RVV(i+1) + Cpa*Ppa(i+1) + Cpp*Ppp(i+1) + Cpv*Ppv(i+1) + Cla*LAP(i+1) + LVV(i+1) + Vu(i+1);
    Plbv(i+1) = splanchicVenous(TBV,Vlbv(i+1),Clbv);

    %Valves
    Qmv(i+1) = valves(LAP(i+1),LVP(i+1),Rla+Rmv);
    Qaov(i+1) = valves(LVP(i+1),Psa(i+1),Raov);
    Qtv(i+1) = valves(RAP(i+1),RVP(i+1),Rra+Rtv);
    Qpulv(i+1) = valves(RVP(i+1),Ppa(i+1),Rpulv);
end