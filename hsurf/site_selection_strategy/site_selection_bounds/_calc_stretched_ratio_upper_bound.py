from ._calc_gap_size_upper_bound import calc_gap_size_upper_bound


def calc_stretched_ratio_upper_bound(
    surface_size: int,
    num_ingests: int,
) -> float:
    """Calculate the worst-possible minimization of the stretched criterion at
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
        The worst-possible minimization of the stretched criterion at
        time step `rank`.
    """
    return calc_gap_size_upper_bound(surface_size, num_ingests)
