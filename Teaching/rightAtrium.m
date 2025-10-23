function dPra = rightAtrium(Psv,Pev,RAP,Rsv,Rev,Ftv,Cra)
    Fin = (Psv - RAP)/Rsv + (Pev - RAP)/Rev;
    dPra = (Fin - Ftv)/Cra;
end