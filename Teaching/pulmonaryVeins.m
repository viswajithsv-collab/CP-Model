function dPpv = pulmonaryVeins(Ppp,Ppv,Pla,Rpp,Rpv,Cpv)
    Fin = (Ppp - Ppv)/Rpp;
    Fout = (Ppv - Pla)/Rpv;
    dPpv = (Fin - Fout)/Cpv;
end