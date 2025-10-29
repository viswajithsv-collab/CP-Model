function dPhv = coronaryVeins(Psvb,Phv,Pra,Rhp,Rhv,Chv)
    fin = (Psvb - Phv)/Rhp;
    fout = (Phv - Pra)/Rhv;
    dPhv = (fin - fout)/Chv;
end