import numpy as np

from ._calc_gap_sizes import calc_gap_sizes_from_gap_bounds
from ._impl import calc_gap_bounds


def _calc_tilted_ratios_from_gaps(
    gap_bounds: np.array, gap_sizes: np.array, num_ingests: int
) -> np.array:
    """Helper for calc_tilted_ratios."""
    gap_highest_ranks = gap_bounds[1:] - 1
    return gap_sizes / np.maximum(num_ingests - 1 - gap_highest_ranks, 1)


def calc_tilted_ratios(retained_ranks: np.array, num_ingests: int) -> np.array:
    """Calculate statistic for tilted retention criterion.

    Parameters
    ----------
    retained_ranks : np.ndarray
        1D array of integer ranks that are retained. Must be non-negative and
        less than or equal to current_rank.
    num_ingests : int
        The number of data items that have been ingested, must be non-negative.

    Returns
    -------
    np.ndarray
        1D floating-point array, largest ratio of gap size to age of dropped
        rank within each gap.

    Notes
    -----
    - The number of tilted ratios returned is always len(retained_ranks) + 1.
    - Ratios are calculated as gap sizes divided by the difference between
      current_rank and the highest rank in each gap, with a minimum
      denominator of 1 to avoid division by zero.

    See Also
    --------
    calc_gap_bounds : Calculate gap bounds for retained ranks and num
    ingests.
    """
    retained_ranks = np.asarray(retained_ranks)
    assert (retained_ranks < num_ingests).all()

    gap_bounds = calc_gap_bounds(retained_ranks, num_ingests)
    gap_sizes = calc_gap_sizes_from_gap_bounds(gap_bounds)
    return _calc_tilted_ratios_from_gaps(gap_bounds, gap_sizes, num_ingests)
