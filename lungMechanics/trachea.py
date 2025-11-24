def trachea(Pt, Pl, Pb, Rlt, Rtb, Ct, dP_pl):
    """Trachea pressure derivative (A31)"""
    Qin = (Pl - Pt) / Rlt
    Qout = (Pt - Pb) / Rtb
    dP_t = dP_pl + (Qin - Qout) / Ct
    return dP_t