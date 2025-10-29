function dPbv = brainVeins(Psvb,Pbv,Pra,Rbp,Rbv,Cbv)
    fin = (Psvb - Pbv)/Rbp;
    fout = (Pbv - Pra)/Rbv;
    dPbv = (fin - fout)/Cbv;
end