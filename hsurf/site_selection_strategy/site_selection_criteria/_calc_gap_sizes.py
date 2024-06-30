import numpy as np

from ._impl import calc_gap_bounds, calc_gap_sizes_from_gap_bounds


def calc_gap_sizes(retained_ranks: np.array, num_depositions: int) -> np.array:
    """Calculate gap sizes among retained ranks, up to first retained rank, and after last retained rank.

    Gap size is defined as the number of missing ranks between two adjacent ranks.

    Parameters
    ----------
    retained_ranks : np.ndarray
        1D array of integer ranks that are retained. Must be non-negative and
        less than `num_depositions`.
    num_depositions : int
        The number of data items that have been ingested, must be non-negative.

    Returns
    -------
    np.ndarray
        1D array of integer gap sizes.

    Notes
    -----
    - The number of gap sizes returned is always len(retained_ranks) + 1.
    - Gap sizes represent the number of ranks between each pair of adjacent
      ranks (including implicit ranks at -1 and `num_depositions`).
    """
    gap_bounds = calc_gap_bounds(retained_ranks, num_depositions)
    return calc_gap_sizes_from_gap_bounds(gap_bounds)
