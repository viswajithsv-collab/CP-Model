function dPmv = muscleVeins(Psvb,Pmv,Pra,Rmvb,Rmv,Cmv)
    fin = (Psvb - Pmv)/Rmvb;
    fout = (Pmv - Pra)/Rmv;
    %fout = f1 + f2;
    dPmv = (fin - fout)/Cmv;
end