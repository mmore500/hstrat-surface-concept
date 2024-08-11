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
    t = max((T + 1).bit_length() - s, 0)  # Current epoch
    h = ctz(T + 1)  # Current hanoi value
    i = T >> (h + 1)  # Hanoi value incidence (i.e., num seen)

    blt = t.bit_length()  # Bit length of t
    epsilon_tau = bit_floor(t << 1) > t + blt  # Correction factor
    tau = blt - epsilon_tau  # Current meta-epoch
    t_0 = (1 << tau) - tau  # Opening epoch of meta-epoch
    epsilon_b = h >= t - t_0  # Correction factor
    b = S >> (tau + epsilon_b) or 1  # Num bunches available to h.v.
    if i >= b:  # If seen more than sties reserved to hanoi value...
        return None  # ... discard without storing

    b_l = i  # Logical bunch index
    # ... i.e., in order filled (increasing nestedness/decreasing init size r)

    v = b_l.bit_length()  # Nestedness depth of physical bunch
    w = (S >> v) * bool(v)  # Bunch spacing at nestedness layer
    o = w >> 1  # Bunch offset at nestedness level
    p = b_l - bit_floor(b_l)  # Bunch position w/in nest layer
    b_p = o + w * p  # Physical bunch index...
    # ... i.e., in left-to-right sequential bunch order

    epsilon_k = bool(b_l)  # Correction factor for zeroth bunch...
    # ... i.e., bunch r=s at site k=0
    k = (  # Site index of bunch
        (b_p << 1) + ((S << 1) - b_p).bit_count() - 1 - epsilon_k
    )

    return k + h  # Calculate placement site...
    # ... where h.v. h is offset within bunch
