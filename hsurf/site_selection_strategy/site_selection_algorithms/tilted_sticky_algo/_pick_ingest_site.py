import warnings

from ..tilted_algo import pick_ingest_site as impl_pick_ingest_site
from ._meta import has_ingest_capacity


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

    res = impl_pick_ingest_site(
        rank, surface_size
    ) or impl_pick_ingest_site(rank + 1, surface_size)

    assert 0 < res < surface_size
    return res
