function dPev = extrasplanchicVenous(Psp,Pev,Pra,dVuev,Rep,Rev,Cev)
    Fin = (Psp - Pev)/Rep;
    f1 = (Pev - Pra)/Rev;
    Fout = f1 + dVuev;
    dPev = (Fin - Fout)/Cev;
end