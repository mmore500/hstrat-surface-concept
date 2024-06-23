from .....pylib import bit_floor, fast_pow2_divide
from ...tilted_algo._impl import get_global_epoch


def calc_next_invasion_rank(rank: int, surface_size: int) -> int:
    """Calculate the next rank where deposited hanoi value will overwrite a
    smaller hanoi value."""
    miniepoch_duration = bit_floor(rank + 1)

    original_num_reservations = surface_size >> 1
    num_dropped = original_num_reservations >> (
        get_global_epoch(rank, surface_size)
    )
    assert miniepoch_duration > num_dropped
    epoch_cadence = fast_pow2_divide(miniepoch_duration, num_dropped)
    assert epoch_cadence

    assert rank
    res = (
        fast_pow2_divide(rank + epoch_cadence + 1, epoch_cadence)
        * epoch_cadence
        - 1
    )
    assert res > rank
    return res
