function dPmv = skeletalmuscleVeins(Psvb,Pmv,Pra,dVumv,Rmvb,Rmv,Cmv)
    fin = (Psvb - Pmv)/Rmvb;
    f1 = (Pmv - Pra)/Rmv;
    f2 = dVumv;
    fout = f1 + f2;
    dPmv = (fin - fout)/Cmv;
end