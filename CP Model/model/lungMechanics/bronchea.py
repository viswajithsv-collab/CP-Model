def bronchea(Pb, Ptr, PA, Rtb, RbA, Cb, dP_pl):
    """Bronchea pressure derivative (A32)"""
    Qin = (Ptr - Pb) / Rtb
    Qout = (Pb - PA) / RbA
    dP_b = dP_pl + (Qin - Qout) / Cb
    return dP_b