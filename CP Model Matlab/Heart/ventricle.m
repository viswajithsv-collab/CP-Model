function [V,P] = ventricle(Emax,Emin,E,Vold,Vu,Fin,Fout,h)
    V = Vold + (Fin - Fout)*h;
    ESP = Emax*(V - Vu);
    EDP = Emin*(V - Vu);
    P = E*ESP + (1-E)*EDP;
end
