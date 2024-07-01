from .....pylib import hanoi, oeis


def _get_global_shifted_epoch(rank: int, surface_size: int) -> int:
    """A.k.a., "meta-epoch"."""
    mini_epoch = max(
        rank.bit_length() - surface_size.bit_length() + 1,
        0,
    )
    # 0 if mini_epoch == 0, else oeis index
    meta_epoch = mini_epoch and oeis.get_a000325_index_of_value(mini_epoch)
    assert (mini_epoch == 0) == (meta_epoch == 0)
    assert (mini_epoch == 1) == (meta_epoch == 1)
    assert (2 <= mini_epoch < 5) == (meta_epoch == 2)
    return meta_epoch


def _get_global_epoch_slow(rank: int, surface_size: int) -> int:
    """Principle-based calculation of the epoch."""
    max_hanoi = hanoi.get_max_hanoi_value_through_index(rank)
    base_hanoi = surface_size.bit_length() - 1
    if max_hanoi < base_hanoi:
        return 0
    else:
        assert max_hanoi - base_hanoi >= 0
        return min(
            oeis.get_a000295_index_of_value(max_hanoi - base_hanoi) + 1,
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
