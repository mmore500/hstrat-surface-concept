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


def get_reservation_position_physical(
    reservation: int, surface_size: int
) -> int:
    """Return the zeroth site of the given reservation, indexed in physical
    order at rank 0."""
    assert surface_size.bit_count() == 1  # power of 2
    assert 0 <= reservation < surface_size // 2 or surface_size <= 2

    if reservation == 0:  # special case
        return 0

    base = 2 * reservation

    # don't remember why isn't >>1 (halve)...
    last_reservation = (surface_size << 1) - 1
    offset = (last_reservation - reservation + 1).bit_count() - 1

    # make first reservation one site longer, to fix elimination order with
    # layering (i.e., delays invasion so that oldest values for a hanoi value
    # are invaded into
    layering_correction = bool(reservation)

    return base + offset - 2 + layering_correction


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

    k = get_reservation_position_physical(physical_reservation, S)
    return k + h
