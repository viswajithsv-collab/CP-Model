def left_atrium(Ppv, LAP, Rpv, Fmv, Cla, Vu_la=0):
    """Left atrium pressure derivative"""
    Fin = (Ppv - LAP) / Rpv
    dPla = (Fin - Fmv) / Cla
    Vla = Cla * LAP + Vu_la  # ✅ Add volume calculation
    return dPla, Vla  # ✅ Return volume too

def right_atrium(Psv, Pev, RAP, Rsv, Rev, Ftv, Cra, Vu_ra=0):
    """Right atrium pressure derivative"""
    Fin = (Psv - RAP) / Rsv + (Pev - RAP) / Rev
    dPra = (Fin - Ftv) / Cra
    Vra = Cra * RAP + Vu_ra  # ✅ Add volume calculation
    return dPra, Vra  # ✅ Return volume too