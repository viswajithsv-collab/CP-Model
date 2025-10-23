function dPpa = pulmonaryArteryRC(Fin,Ppa,Ppp,Rpa,Cpa)
    Fout = (Ppa - Ppp)/Rpa;
    dPpa = (Fin - Fout)/Cpa;
end