from ._impl import calc_gap_ratio_lower_bound


def calc_tilted_ratio_lower_bound(
    rank: int,
    surface_size: int,
) -> float:
    """Calculate the best-possible minimization of the tilted criterion at
    time step `rank`.

    Parameters
    ----------
    rank : int
        The current time step.
    surface_size : int
        The maximum number of items that can be retained.

    Returns
    -------
    int
        The best-possible minimization of the tilted criterion at
        time step `rank`.

    See Also
    --------
    calc_gap_ratio_lower_bound : Implementation, shared with stretched
    criterion.
    """
    return calc_gap_ratio_lower_bound(rank, surface_size)
