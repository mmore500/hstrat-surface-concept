from ..tilted_algo import pick_ingest_site as impl_pick_ingest_site


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
    res = impl_pick_ingest_site(
        rank, surface_size
    ) or impl_pick_ingest_site(rank + 1, surface_size)

    assert 0 < res < surface_size
    return res
