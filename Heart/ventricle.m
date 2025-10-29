function [V,P,Pmax,R] = ventricle(Emax,E,Vold,Vu,Fin,Fout,kr,ke,P0,h)
    V = Vold + (Fin - Fout)*h;
    ESP = Emax*(V - Vu);
    EDP = P0*(exp(ke*V)-1);
    Pmax = E*ESP + (1-E)*EDP;
    R = kr*Pmax;
    P = Pmax - R*Fout;
end