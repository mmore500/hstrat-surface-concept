from .....pylib import hanoi, oeis
from ...tilted_algo._impl import get_global_epoch


def calc_next_invasion_rank(rank: int, surface_size: int) -> int:
    """Calculate the next rank where deposited hanoi value will overwrite a
    smaller hanoi value."""
    epoch = get_global_epoch(rank, surface_size)
    assert epoch
    min_hanoi_invader = oeis.get_a062289_value_at_index(epoch - 1)
    invasion_rank = hanoi.get_index_of_next_hanoi_value_geq_to(
        min_hanoi_invader, rank
    )
    return invasion_rank
