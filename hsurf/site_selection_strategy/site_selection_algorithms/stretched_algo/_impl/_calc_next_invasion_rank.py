from .....pylib import hanoi, oeis
from ...tilted_algo._impl import get_global_epoch, get_hanoi_num_reservations


def calc_next_invasion_rank(rank: int, surface_size: int) -> int:
    """Calculate the next rank where deposited hanoi value will overwrite a
    smaller hanoi value."""
    epoch = get_global_epoch(rank, surface_size)
    assert epoch
    min_hanoi_invader = oeis.get_a062289_value_at_index(epoch - 1)
    assert min_hanoi_invader
    while get_hanoi_num_reservations(
        rank, surface_size, min_hanoi_invader
    ) <= hanoi.get_incidence_count_of_hanoi_value_through_index(
        min_hanoi_invader, rank
    ):
        min_hanoi_invader += 1
    invasion_rank = hanoi.get_index_of_next_hanoi_value_geq_to(
        min_hanoi_invader, rank
    )
    return invasion_rank
