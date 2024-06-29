def calc_gap_size_lower_bound(surface_size: int, num_depositions: int) -> int:
    """Calculate the lower bound of gap size at time step `rank`.

    Parameters
    ----------
    surface_size : int
        The maximum number of items that can be retained.
    num_depositions : int
        The number of data items that have been ingested.

    Returns
    -------
    int
        The lowest-possible largest set of consecutive dropped elements.
    """
    naive = rank // surface_size
    res = (max(rank + 1 - surface_size, 0) + surface_size) // (surface_size + 1)
    # res = (max(rank + 1 - surface_size, 0) + surface_size) // (surface_size + 1)
    # aka
    res = (rank + 1) // (surface_size + 1)
    assert res <= naive
    return res
