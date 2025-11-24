def phases(b, Ti):
    """Respiratory phase indicator"""
    if b <= Ti:
        a = 1  # Inspiration
    else:
        a = -1  # Expiration
    return a