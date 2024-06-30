from ....pylib import fast_pow2_mod
from ..steady_algo import pick_ingest_site as steady_impl
from ..tilted_algo import pick_ingest_site as tilted_mpl


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
    assert surface_size.bit_count() == 1
    assert surface_size >= 4  # need 2 per side

    if rank == 0:
        return 0
    if fast_pow2_mod(rank, 2) == 0:
        return steady_impl(rank >> 1, surface_size >> 1)
    else:
        return tilted_mpl(rank >> 1, surface_size >> 1) + (surface_size >> 1)
