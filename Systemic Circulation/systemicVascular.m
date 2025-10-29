function dPsvb = systemicVascular(Psvb, Psa, Psv, Pev, Pmv, Pbv, Phv, Rsa, Rsvb, Revb, Rmvb, Rbvb, Rhvb, Csvb, Cevb, Cmvb, Cbvb, Chvb)
%P = [Psvb(P1), Psa(P2), Psv(P3), Pev(P4), Pmv(P5), Pbv(P6), Phv(P7)]
%R = [Rsa(R1), Rsp(R2), Rep(R3), Rmp(R4), Rbp(R5), Rhp(R6)]
%C = [Csp(C1), Cep(C2), Cmp(C3), Cbp(C4), Chp(C5)]
    f1 = (Psvb - Psv)/Rsvb;
    f2 = (Psvb - Pev)/Revb;
    f3 = (Psvb - Pmv)/Rmvb;
    f4 = (Psvb - Pbv)/Rbvb;
    f5 = (Psvb - Phv)/Rhvb;
    Fout = f1 + f2 + f3 + f4 + f5;
    Fin = (Psa - Psvb)/Rsa;
    Ctot = Csvb + Cevb + Cmvb + Cbvb + Chvb;
    dPsvb = (Fin - Fout)/Ctot;
end