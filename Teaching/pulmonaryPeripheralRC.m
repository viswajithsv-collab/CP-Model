function  dPpp = pulmonaryPeripheralRC(Ppa,Ppp,Ppv,Rpa,Rpp,Cpp)
    Fin = (Ppa - Ppp)/Rpa;
    Fout = (Ppp - Ppv)/Rpp;
    dPpp = (Fin - Fout)/Cpp;
end