import typing


def ctz(x: int) -> int:
    """Count trailing zeros."""
    assert x > 0
    return (x & -x).bit_length() - 1


def get_hanoi_num_reservations(
    rank: int, surface_size: int, hanoi_value: typing.Optional[int] = None
) -> int:
    """Return the number of reservations remaining at the given rank.

    Either the current global-level reservation count, or double it if the
    hanoi value is uninvaded."""
    epoch = get_global_epoch(rank, surface_size)
    grc = get_global_num_reservations(rank, surface_size)

    if epoch == 0:
        return grc

    if hanoi_value is None:
        hanoi_value = get_hanoi_value_at_index(rank)
    max_uninvaded = (1 << epoch) - 2  # 0, 2, 6, 14, ...
    assert max_uninvaded >= 0
    if hanoi_value > max_uninvaded:
        return grc

    reservation0_at = get_max_hanoi_value_through_index(rank)
    assert epoch > 0
    idx = 1 << (epoch - 1)  # 1, 2, 4, 8, ...
    assert idx > 0
    reservation0_begin = (
        # -1 undoes correction for extra reservation 0 slot
        get_reservation_position_physical(idx, surface_size)
        - 1
    )
    reservation0_progress = reservation0_at - reservation0_begin
    if hanoi_value <= reservation0_progress:
        return grc

    return 2 * grc


def get_longevity_offset_of_level(
    level: int,
    num_indices: int,
) -> int:
    """How many physical sites from beginning does the first element of the
    nth level occur?"""
    # alternate impl: (num_indices >> level) * bool(level)
    return (num_indices >> level) & ~num_indices


def get_longevity_level_of_index(index: int) -> int:
    """What physical nesting layer does the logical index map to?"""
    return index.bit_length()


def bit_floor(n: int) -> int:
    """Calculate the largest power of two not greater than n.

    If zero, returns zero.
    """
    # adapted from https://github.com/mmore500/hstrat/blob/e9c2994c7a6514162f1ab685d88c374372dc1cf0/hstrat/_auxiliary_lib/_bit_floor.py
    mask = 1 << (n >> 1).bit_length()
    return n & mask


# related to https://oeis.org/A181733
# see also https://oeis.org/A139709 and https://oeis.org/A092323
def get_longevity_mapped_position_of_index(index: int, num_indices: int) -> int:
    """Which physical site in the sequence does the `index`th logical entry map
    to?"""
    longevity_level = get_longevity_level_of_index(index)

    # see get_powersof2triangle_val_at_index
    position_within_level = index - bit_floor(index)

    offset = get_longevity_offset_of_level(longevity_level, num_indices)
    spacing = offset << 1
    res = offset + spacing * position_within_level
    assert res.bit_count() == index.bit_count()
    return res


def fast_pow2_mod(dividend: int, divisor: int) -> int:
    """Perform fast mod using bitwise operations.

    Parameters
    ----------
    dividend : int
        The dividend of the mod operation.
    divisor : int
        The divisor of the mod operation. Must be a positive integer and a
        power of 2.

    Returns
    -------
    int
        The remainder of dividing the dividend by the divisor.

    Examples
    --------
    >>> fast_pow2_mod(16, 4)
    0

    >>> fast_pow2_mod(17, 4)
    1

    >>> fast_pow2_mod(0, 4)
    0

    >>> fast_pow2_mod(3, 4)
    3
    """
    assert divisor >= 1
    assert divisor.bit_count() == 1

    return dividend + abs(dividend * divisor) & (divisor - 1)


def get_reservation_position_logical(
    reservation: int, surface_size: int
) -> int:
    """Return the zeroth site of the given reservation, indexed in logical
    order (persistence order)."""
    assert surface_size.bit_count() == 1  # power of 2
    num_reservations = surface_size >> 1
    physical_reservation = get_longevity_mapped_position_of_index(
        reservation, num_reservations
    )
    return get_reservation_position_physical(physical_reservation, surface_size)


def get_global_num_reservations(rank: int, surface_size: int) -> int:
    """Return the number of global-level reservations at the given rank."""
    epoch = get_global_epoch(rank, surface_size)
    return get_global_num_reservations_at_epoch(epoch, surface_size)


def get_global_num_reservations_at_epoch(epoch: int, surface_size: int) -> int:
    assert surface_size.bit_count() == 1  # power of 2
    return surface_size >> (1 + epoch)


# see https://oeis.org/A000295
def get_a000325_value_at_index(n: int) -> int:
    """Return the value of A000325 at the given index.

    A000325(n) = 2^n - n.
    """
    return (1 << n) - n  # Chai Wah Wu, https://oeis.org/A000325


# see https://oeis.org/A000325
def get_a000325_index_of_value(v: int) -> int:
    """Return the greatest index of A000325 with value `<= v`.

    v must be positive.
    """
    assert v > 0
    ansatz = (v).bit_length()
    correction = get_a000325_value_at_index(ansatz) > v
    return ansatz - correction


# see https://oeis.org/A000295
def get_a000295_value_at_index(n: int) -> int:
    """Return the value of A000295 at the given index.

    Note: uses -1 as the first index, i.e., skips zeroth element.
    """
    n += 1
    return (1 << n) - n - 1


def get_a000295_index_of_value(v: int) -> int:
    """Return the greatest index of A000295 with value `<= v`.

    Note: uses -1 as the first index, i.e., skips zeroth element.
    """
    ansatz = (v + 1).bit_length() - 1
    correction = get_a000295_value_at_index(ansatz) > v
    return ansatz - correction


def _get_global_shifted_mini_epoch(rank: int, surface_size: int) -> int:
    """A.k.a., "epoch" in writeup."""
    return max(
        rank.bit_length() - surface_size.bit_length() + 1,
        0,
    )


def _get_global_shifted_epoch(rank: int, surface_size: int) -> int:
    """A.k.a., "meta-epoch" in writeup."""
    mini_epoch = _get_global_shifted_mini_epoch(rank, surface_size)
    # 0 if mini_epoch == 0, else oeis index
    meta_epoch = mini_epoch and get_a000325_index_of_value(mini_epoch)
    assert (mini_epoch == 0) == (meta_epoch == 0)
    assert (mini_epoch == 1) == (meta_epoch == 1)
    assert (2 <= mini_epoch < 5) == (meta_epoch == 2)
    return meta_epoch


def _get_global_epoch_slow(rank: int, surface_size: int) -> int:
    """Principle-based calculation of the epoch."""
    max_hanoi = get_max_hanoi_value_through_index(rank)
    base_hanoi = surface_size.bit_length() - 1
    if max_hanoi < base_hanoi:
        return 0
    else:
        assert max_hanoi - base_hanoi >= 0
        return min(
            get_a000295_index_of_value(max_hanoi - base_hanoi) + 1,
            surface_size.bit_length() - 2,
        )


def get_global_epoch(rank: int, surface_size: int) -> int:
    """Return the reservation-halving epoch of the given rank.

    Rank zero is at 0th epoch. Epochs count up with each reservation count
    halving.

    Note: uses original, unshifted definition of epoch.
    """
    assert surface_size.bit_count() == 1  # power of 2
    fast = min(
        _get_global_shifted_epoch(rank + 1, surface_size),
        surface_size.bit_length() - 2,
    )  # rank + 1 and min correction are due to unshifted epoch definition

    assert fast == _get_global_epoch_slow(rank, surface_size)
    return fast


# see https://oeis.org/A048881
def get_a048881_value_at_index(n: int) -> int:
    # Chai Wah Wu, Nov 15 2022
    return (n + 1).bit_count() - 1


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
    offset = get_a048881_value_at_index(last_reservation - reservation)

    # make first reservation one site longer, to fix elimination order with
    # layering (i.e., delays invasion so that oldest values for a hanoi value
    # are invaded into
    layering_correction = bool(reservation)

    return base + offset - 2 + layering_correction


def get_max_hanoi_value_through_index(n: int) -> int:
    """What is the largest hanoi value that occurs at indices up to and
    including index n?

    See `get_hanoi_value_at_index` for notes on zero-based variant of Hanoi sequence used.
    """
    # offset = 2**value - 1
    # offset + 1 = 2**value
    # floorlog2(offset + 1) = value
    return (n + 1).bit_length() - 1


def impl_pick_ingest_site(
    rank: int,
    surface_size: int,
) -> int:
    """Pick the ingest site on a surface for a given rank.

    This function calculates a ingest site based on the rank and the
    surface size.

    Parameters
    ----------
    rank : int
        The number of time steps elapsed.
    surface_size : int
        The size of the surface on which ingest is to take place.

        Must be even power of two.

    Returns
    -------
    int
        Ingest site within surface.
    """
    num_reservations = get_hanoi_num_reservations(rank, surface_size)

    incidence = get_hanoi_value_incidence_at_index(rank)
    hanoi_value = get_hanoi_value_at_index(rank)

    reservation = fast_pow2_mod(incidence, num_reservations)
    res = (
        get_reservation_position_logical(reservation, surface_size)
        + hanoi_value
    )

    assert 0 <= res < surface_size
    return res


def pick_ingest_site(
    rank: int,
    surface_size: int,
) -> int:
    """Pick the ingest site on a surface for a given rank.

    This function calculates a ingest site based on the rank and the
    surface size.

    Parameters
    ----------
    rank : int
        The number of time steps elapsed.
    surface_size : int
        The size of the surface on which ingest is to take place.

        Must be even power of two.

    Returns
    -------
    int
        Ingest site within surface.
    """

    num_reservations = get_hanoi_num_reservations(rank, surface_size)

    incidence = get_hanoi_value_incidence_at_index(rank)

    if incidence >= num_reservations:
        return surface_size

    res = impl_pick_ingest_site(rank, surface_size)
    assert 0 <= res < surface_size
    return res


def get_hanoi_value_incidence_at_index(n: int) -> int:
    """How many times has the hanoi value at index n already been encountered?

    Assumes zero-indexing convention. See `get_hanoi_value_at_index` for notes
    on zero-based variant of Hanoi sequence used.
    """
    # equiv to n // 2 ** (get_hanoi_value_at_index(n) + 1)
    return n >> (get_hanoi_value_at_index(n) + 1)


def get_hanoi_value_at_index(n: int) -> int:
    """Get value of zero-indexed, zero-based Hanoi sequence in constant time.

    This sequence is [A007814](https://oeis.org/A007814) in the Online
    Encyclopedia of Integer Sequences. Equivalent to the Hanoi sequence
    ([A001511](https://oeis.org/A00151)), with all values less one. Indexing
    assumes zero-based convention.
    """
    n += 1
    return (n & -n).bit_length() - 1


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
    res = pick_ingest_site(T, S)
    return None if res == S else res
