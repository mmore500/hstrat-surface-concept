from ._impl import calc_gap_ratio_lower_bound


def calc_stretched_ratio_lower_bound(
    surface_size: int,
    num_ingests: int,
) -> float:
    """Calculate the best-possible minimization of the stretched criterion at
    time step `rank`.

    Parameters
    ----------
    surface_size : int
        The maximum number of items that can be retained.
    num_ingests : int
        The number of data items that have been ingested.

    Returns
    -------
    int
        The best-possible minimization of the stretched criterion at
        time step `rank`.

    See Also
    --------
    calc_gap_ratio_lower_bound : Implementation, shared with tilted criterion.
    """
    return calc_gap_ratio_lower_bound(surface_size, num_ingests)
