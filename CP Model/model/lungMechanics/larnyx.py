def larynx(Pl, Pao, Ptr, Rml, Rlt, Cl):
    """Larynx pressure derivative (A30)"""
    Qin = (Pao - Pl) / Rml
    Qout = (Pl - Ptr) / Rlt
    dPl = (Qin - Qout) / Cl
    return dPl