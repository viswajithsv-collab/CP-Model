function dPpa = pulmonaryArtery(Qin,Ppa,Ppp,Rpa,Cpa)
    Fout = (Ppa - Ppp)/Rpa;
    dPpa = (Qin - Fout)/Cpa;
end