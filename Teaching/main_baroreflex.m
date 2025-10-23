Constants;
HeartVariables;
Initialize;
BaroreflexConstants;
HR = 90;
T = 60/HR;
H = HR;
t = 0:0.001:100;
h = 0.001;
%Double-Hill Function
alpha = [0.103,0.408];
n = [1.9,21.9];
E = phi1(t,HR,alpha,n);
w = h/H;
x = 0;
y = 0;
z = 0;
a1 = 0;
a2 = 0;
m = 0;
o = 0;
p = 0;
q = 0;
e = 0;

Emaxlv = 2.4;
Emaxrv = 1.8;
Rsp = 2.49;
Rep = 0.78;
Vusv = 1435.4;
Vuev = 1537;

for i = 1:length(t)-1
    E1(i) = activation(1.12,w(i),H(i),alpha,n);
    
    %Left Atrium
    dPla = leftAtrium(Ppv(i),LAP(i),Rpv,Fmv(i),Cla);
    LAP(i+1) = LAP(i) + dPla*h;

    %Right Atrium
    dPra = rightAtrium(Psv(i),Pev(i),RAP(i),Rsv,Rev,Ftv(i),Cra);
    RAP(i+1) = RAP(i) + dPra*h;

    %Left Ventricle
    [LVV(i+1),LVP(i+1),LVPmax(i+1),Rlv(i+1)] = ventricle(Emaxlv(i),E1(i),LVV(i),Vulv,Fmv(i),Faov(i),krlv,kelv,P0lv,h);

    %Right Ventricle
    [RVV(i+1),RVP(i+1),RVPmax(i+1),Rrv(i+1)] = ventricle(Emaxrv(i),E1(i),RVV(i),Vurv,Ftv(i),Fpulv(i),krrv,kerv,P0rv,h);

    %Systemic Circulation
    [dPsa,dFsa] = systemicArtery(Faov(i),Fsa(i),Psa(i),Psp(i),Rsa,Csa,Lsa);
    Psa(i+1) = Psa(i)+dPsa*h;
    Fsa(i+1) = Fsa(i)+dFsa*h;
    dPsp = systemicPeripheral(Fsa(i),Psp(i),Psv(i),Pev(i),Rsp(i),Rep(i),Csp,Cep);
    Psp(i+1) = Psp(i)+dPsp*h;
    %dPev = extrasplanchicVenous(Psp(i),Pev(i),RAP(i),dVuev(i),Rep,Rev,Cev);
    dPev = extrasplanchicVenous(Psp(i),Pev(i),RAP(i),0,Rep(i),Rev,Cev);
    Pev(i+1) = Pev(i)+dPev*h;

    %Pulmonary Circulation
    [dPpa,dFpa] = pulmonaryArtery(Fpulv(i),Fpa(i),Ppa(i),Ppp(i),Rpa,Cpa,Lpa);
    Ppa(i+1) = Ppa(i)+dPpa*h;
    Fpa(i+1) = Fpa(i)+dFpa*h;
    dPpp = pulmonaryPeripheral(Fpa(i),Ppp(i),Ppv(i),Rpp,Cpp);
    Ppp(i+1) = Ppp(i)+dPpp*h;
    dPpv = pulmonaryVeins(Ppp(i),Ppv(i),LAP(i),Rpp,Rpv,Cpv);
    Ppv(i+1) = Ppv(i)+dPpv*h;

    %Unstressed Volume
    %Vu(i+1) = Vusa + Vusp + Vuep + Vusv(i+1) + Vuev(i+1) + Vura + Vupa + Vupp + Vupv + Vula;
    Vu(i+1) = Vusa + Vusp + Vuep + Vusv(i) + Vuev(i) + Vura + Vupa + Vupp + Vupv + Vula;
    %dVuev(i+1) = (Vuev(i+1) - Vuev(i))/h;

    %Splanchic Venous Circulation
    Vsv(i+1) = Csa*Psa(i+1) + (Csp+Cep)*Psp(i+1) + Cev*Pev(i+1) + Cra*RAP(i+1) + RVV(i+1) + Cpa*Ppa(i+1) + Cpp*Ppp(i+1) + Cpv*Ppv(i+1) + Cla*LAP(i+1) + LVV(i+1) + Vu(i+1);
    Psv(i+1) = splanchicVenous(TBV,Vsv(i+1),Csv);

    %Valves
    Fmv(i+1) = valves(LAP(i+1),LVP(i+1),Rla);
    Faov(i+1) = valves(LVPmax(i+1),Psa(i+1),Rlv(i+1));
    Ftv(i+1) = valves(RAP(i+1),RVP(i+1),Rra);
    Fpulv(i+1) = valves(RVPmax(i+1),Ppa(i+1),Rrv(i+1));

    % dPaff = linearDerivative(Psa(i),dPsa,Paff,taup,tauz);
    % Paff = Paff + dPaff*h;
    Paff = linearDerivative(Psa(i),dPsa,Paff,taup,tauz,h);
    fcs = afferentPathway(Paff,Pn,fmin,fmax,ka);
    fes = efferentSympathetic(fcs,fes0,fesinf,kes);
    fev = efferentVagal(fcs,fcs0,fev0,fevinf,kev);

    %Sympathetic Effector
    sigma_Emaxlv(i) = effectorSympathetic(GEmaxlv,fes,t(i),DEmaxlv,fesmin);
    sigma_Emaxrv(i) = effectorSympathetic(GEmaxrv,fes,t(i),DEmaxrv,fesmin);
    sigma_Rsp(i) = effectorSympathetic(GRsp,fes,t(i),DRsp,fesmin);
    sigma_Rep(i) = effectorSympathetic(GRep,fes,t(i),DRep,fesmin);
    sigma_Vusv(i) = effectorSympathetic(GVusv,fes,t(i),DVusv,fesmin);
    sigma_Vuev(i) = effectorSympathetic(GVuev,fes,t(i),DVuev,fesmin);
    sigma_Ts(i) = effectorSympathetic(GTs,fes,t(i),DTs,fesmin);

    %Vagal Effector
    sigma_Tv(i) = effectorVagal(GTv,fev,t(i),DTv);

    %Sympathetic Regulation
    theta_Emaxlv(i+1) = theta_Emaxlv(i) + Regulation(theta_Emaxlv(i),sigma_Emaxlv(i),tauEmaxlv)*h;
    Emaxlv(i+1) = theta_Emaxlv(i+1) + Emaxlv(1);
    theta_Emaxrv(i+1) = theta_Emaxrv(i) + Regulation(theta_Emaxrv(i),sigma_Emaxrv(i),tauEmaxrv)*h;
    Emaxrv(i+1) = theta_Emaxrv(i+1) + Emaxrv(1);
    theta_Rsp(i+1) = theta_Rsp(i) + Regulation(theta_Rsp(i),sigma_Rsp(i),tauRsp)*h;
    Rsp(i+1) = theta_Rsp(i+1) + Rsp(1);
    theta_Rep(i+1) = theta_Rep(i) + Regulation(theta_Rep(i),sigma_Rep(i),tauRep)*h;
    Rep(i+1) = theta_Rep(i+1) + Rep(1);
    theta_Vusv(i+1) = theta_Vusv(i) + Regulation(theta_Vusv(i),sigma_Vusv(i),tauVusv)*h;
    Vusv(i+1) = theta_Vusv(i+1) + Vusv(1);
    theta_Vuev(i+1) = theta_Vuev(i) + Regulation(theta_Vuev(i),sigma_Vuev(i),tauVuev)*h;
    Vuev(i+1) = theta_Vuev(i+1) + Vuev(1);
    theta_Ts(i+1) = theta_Ts(i) + Regulation(theta_Ts(i),sigma_Ts(i),tauTs)*h;
    theta_Tv(i+1) = theta_Tv(i) + Regulation(theta_Tv(i),sigma_Tv(i),tauTv)*h;
    T(i+1) = theta_Ts(i+1) + theta_Tv(i+1) + T(1);
    H(i+1) = 60/T(i+1);
    w(i+1) = w(i) + h/T(i+1);
end