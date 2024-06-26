import numpy as np


def calc_gap_bounds(retained_ranks: np.array, num_ingests: int) -> np.array:
    """Calculate gap bounds for retained ranks and current rank.

    Parameters
    ----------
    retained_ranks : np.ndarray
        1D array of integer ranks that are retained, must be non-negative and
        less than num_ingests.
    num_ingests : int
        The number of data items that have been ingested, must be non-negative.

    Returns
    -------
    np.ndarray
        1D array of integer gap bounds, including -1 at the start and
        `num_ingests` at the end.
    """
    retained_ranks = np.asarray(retained_ranks)
    assert (retained_ranks >= 0).all()
    assert (retained_ranks < num_ingests).all()

    sorted_ranks = np.sort(retained_ranks)
    return np.array([-1, *sorted_ranks, num_ingests], dtype=int)
