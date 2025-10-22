def alveoli(PA, Pb, RbA, CA, dP_pl):
    """Alveoli pressure derivative (A33)"""
    Qin = (Pb - PA) / RbA
    dP_A = dP_pl + Qin / CA
    return dP_A