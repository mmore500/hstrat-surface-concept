def calc_gap_size_upper_bound(surface_size: int, num_ingests: int) -> int:
    """Calculate the upper bound of gap size at time step `rank`.

    Parameters
    ----------
    surface_size : int
        The maximum number of items that can be retained.
    num_ingests : int
        The number of data items that have been ingested.

    Returns
    -------
    int
        The highest-possible largest set of consecutive dropped elements.
    """
    return num_ingests
