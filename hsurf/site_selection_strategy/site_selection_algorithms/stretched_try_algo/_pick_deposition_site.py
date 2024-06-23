from ....pylib import hanoi
from ..tilted_algo import pick_deposition_site as impl_pick_deposition_site
from ..tilted_algo._impl import get_hanoi_num_reservations
from ._impl import calc_next_invasion_rank


def pick_deposition_site(
    rank: int,
    surface_size: int,
) -> int:
    """Pick the deposition site on a surface for a given rank.

    This function calculates a deposition site based on the rank and the
    surface size.

    Parameters
    ----------
    rank : int
        The number of time steps elapsed.
    surface_size : int
        The size of the surface on which deposition is to take place.

        Must be even power of two.

    Returns
    -------
    int
        Deposition site within surface.
    """
    num_reservations = get_hanoi_num_reservations(rank, surface_size)

    incidence = hanoi.get_hanoi_value_incidence_at_index(rank)

    if incidence >= num_reservations:
        return surface_size

    res = impl_pick_deposition_site(rank, surface_size)
    assert 0 <= res < surface_size
    return res
