import numpy as np

from ._impl import calc_gap_bounds, calc_gap_sizes_from_gap_bounds


def calc_gap_sizes(retained_ranks: np.array, current_rank: int) -> np.array:
    """Calculate gap sizes among retained ranks, up to first retained rank, and after last retained rank.

    Gap size is defined as the number of missing ranks between two adjacent ranks.

    Parameters
    ----------
    retained_ranks : np.ndarray
        1D array of integer ranks that are retained. Must be non-negative and
        less than or equal to current_rank.
    current_rank : int
        The current rank. Must be non-negative.

    Returns
    -------
    np.ndarray
        1D array of integer gap sizes.

    Notes
    -----
    - If retained_ranks is empty, returns an empty array.
    - Otherwise, the number of gap sizes returned is always len(retained_ranks)
      + 1.
    - Gap sizes represent the number of ranks between each pair of adjacent
      ranks (including implicit ranks at -1 and current_rank + 1).
    """
    if retained_ranks.size == 0:
        return np.array([], dtype=int)

    gap_bounds = calc_gap_bounds(retained_ranks, current_rank)
    return calc_gap_sizes_from_gap_bounds(gap_bounds)
