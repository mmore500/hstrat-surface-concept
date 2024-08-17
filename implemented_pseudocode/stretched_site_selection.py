import typing


def ctz(x: int) -> int:
    """Count trailing zeros."""
    assert x > 0
    return (x & -x).bit_length() - 1


def bit_floor(n: int) -> int:
    """Calculate the largest power of two not greater than n.

    If zero, returns zero.
    """
    mask = 1 << (n >> 1).bit_length()
    return n & mask


def stretched_site_selection(S: int, T: int) -> typing.Optional[int]:
    """Site selection algorithm for stretched curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : int
        Current logical time. Must be less than 2**S - 1.

    Returns
    -------
    typing.Optional[int]
        Selected site, if any.
    """
    s = S.bit_length() - 1
    t = max((T).bit_length() - s, 0)  # Current epoch
    h = ctz(T + 1)  # Current hanoi value
    i = T >> (h + 1)  # Hanoi value incidence (i.e., num seen)

    blt = t.bit_length()  # Bit length of t
    epsilon_tau = bit_floor(t << 1) > t + blt  # Correction factor
    tau = blt - epsilon_tau  # Current meta-epoch
    b = S >> (tau + 1) or 1  # Num bunches available to h.v.
    if i >= b:  # If seen more than sites reserved to hanoi value...
        return None  # ... discard without storing

    b_l = i  # Logical bunch index...
    # ... i.e., in order filled (increasing nestedness/decreasing init size r)

    # Need to calculate physical bunch index...
    # ... i.e., position among bunches left-to-right in buffer space
    v = b_l.bit_length()  # Nestedness depth level of physical bunch
    w = (S >> v) * bool(v)  # Num bunches spaced between bunches in nest level
    o = w >> 1  # Offset of nestedness level in physical bunch order
    p = b_l - bit_floor(b_l)  # Bunch position within nestedness level
    b_p = o + w * p  # Physical bunch index...
    # ... i.e., in left-to-right sequential bunch order

    # Need to calculate buffer position of b_p'th bunch
    epsilon_k = bool(b_l)  # Correction factor for zeroth bunch...
    # ... i.e., bunch r=s at site k=0
    k = (  # Site index of bunch
        (b_p << 1) + ((S << 1) - b_p).bit_count() - 1 - epsilon_k
    )

    return k + h  # Calculate placement site...
    # ... where h.v. h is offset within bunch
