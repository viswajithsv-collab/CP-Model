function  dPpvb = pulmonaryVascular(Ppa,Ppvb,Ppv,Rpa,Rpp,Cpp)
    Fin = (Ppa - Ppvb)/Rpa;
    Fout = (Ppvb - Ppv)/Rpp;
    dPpvb = (Fin - Fout)/Cpp;
end