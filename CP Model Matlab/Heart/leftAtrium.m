function dPla = leftAtrium(Ppv,LAP,Rpv,Fmv,Cla)
    Fin = (Ppv - LAP)/Rpv;
    dPla = (Fin - Fmv)/Cla;
end