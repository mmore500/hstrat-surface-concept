import typing


def ctz(x: int) -> int:
    """Count trailing zeros."""
    assert x > 0
    return (x & -x).bit_length() - 1


def bit_floor(n: int) -> int:
    """Calculate the largest power of two not greater than n.

    If zero, returns zero.
    """
    # adapted from https://github.com/mmore500/hstrat/blob/e9c2994c7a6514162f1ab685d88c374372dc1cf0/hstrat/_auxiliary_lib/_bit_floor.py
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
    t = (T + 1).bit_length() - s  # Current epoch (or negative)
    h = ctz(T + 1)  # Current hanoi value
    i = T >> (h + 1)  # Hanoi value incidence
    if t > 0:
        tau_ansatz = t.bit_length()
        epsilon_tau = (1 << tau_ansatz) - tau_ansatz > t  # Correction
        tau = tau_ansatz - epsilon_tau  # Current meta-epoch
        t_0 = (1 << tau) - tau  # Opening epoch of meta-epoch
        assert t_0 <= t
        epsilon_b = h >= t - t_0  # Correction factor
        b = S >> (tau + epsilon_b)  # Num bunches
        if i >= b:
            return None

    level = i.bit_length()
    position_within_level = i - bit_floor(i)
    num_reservations = S >> 1
    offset = (num_reservations >> level) * bool(level)
    spacing = offset << 1
    physical_reservation = offset + spacing * position_within_level
    k = (
        (physical_reservation << 1)
        + ((S << 1) - physical_reservation).bit_count()
        - 1
        - bool(i)
    )

    return k + h
