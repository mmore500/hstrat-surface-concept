import warnings

from .....pylib import fast_pow2_mod, hanoi
from .._impl import (
    get_hanoi_num_reservations,
    get_reservation_position_logical,
)
from .._meta import has_ingest_capacity


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
    if not has_ingest_capacity(surface_size, rank + 1):
        warnings.warn(
            "Rank exceeds ingest capacity. Either surface size is not "
            "supported or too many ingestions have elapsed.",
        )

    num_reservations = get_hanoi_num_reservations(rank, surface_size)

    incidence = hanoi.get_hanoi_value_incidence_at_index(rank)
    hanoi_value = hanoi.get_hanoi_value_at_index(rank)

    reservation = fast_pow2_mod(incidence, num_reservations)
    res = (
        get_reservation_position_logical(reservation, surface_size)
        + hanoi_value
    )

    assert 0 <= res < surface_size
    return res
