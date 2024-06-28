import numpy as np


def calc_gap_bounds(retained_ranks: np.array, current_rank: int) -> np.array:
    """Calculate gap bounds for retained ranks and current rank.

    Parameters
    ----------
    retained_ranks : np.ndarray
        1D array of integer ranks that are retained, must be non-negative and
        less than or equal to current_rank.
    current_rank : int
        The current rank, must be non-negative.

    Returns
    -------
    np.ndarray
        1D array of integer gap bounds, including -1 at the start and
        (current_rank + 1) at the end.
    """
    if retained_ranks.size == 0:
        return np.array([], dtype=int)

    assert (retained_ranks >= 0).all()
    assert (retained_ranks <= current_rank).all()

    sorted_ranks = np.sort(retained_ranks)
    return np.array([-1, *sorted_ranks, current_rank + 1])
