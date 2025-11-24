def valves(Pin, Pout, R):
    """
    Unidirectional valve flow

    Parameters:
    - Pin: upstream pressure
    - Pout: downstream pressure
    - R: valve resistance
    """
    if Pin <= Pout:
        F = 0
    else:
        F = (Pin - Pout) / R
    return F