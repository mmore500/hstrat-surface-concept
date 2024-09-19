import math


def calc_gap_size_lower_bound(surface_size: int, num_ingests: int) -> int:
    """Calculate the lower bound of gap size at time step `rank`.

    Parameters
    ----------
    surface_size : int
        The maximum number of items that can be retained.
    num_ingests : int
        The number of data items that have been ingested.

    Returns
    -------
    int
        The lowest-possible largest set of consecutive dropped elements.
    """
    naive = num_ingests // surface_size
    # res = (max(num_ingests - surface_size, 0) + surface_size) // (surface_size + 1)
    # aka
    res = num_ingests // (surface_size + 1)
    assert res <= naive
    assert res == math.ceil(
        max(num_ingests - surface_size, 0) / (surface_size + 1),
    )
    return res
