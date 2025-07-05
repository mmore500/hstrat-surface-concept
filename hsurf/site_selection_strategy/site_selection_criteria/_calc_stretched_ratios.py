import numpy as np

from ._calc_gap_sizes import calc_gap_sizes_from_gap_bounds
from ._impl import calc_gap_bounds


def _calc_stretched_ratios_from_gaps(
    gap_bounds: np.array, gap_sizes: np.array
) -> np.array:
    """Helper for calc_stretched_ratios."""
    gap_lowest_ranks = gap_bounds[:-1] + 1
    return gap_sizes / np.maximum(gap_lowest_ranks, 1)


def calc_stretched_ratios(
    retained_ranks: np.array, num_ingests: int
) -> np.array:
    """Calculate statistic for stretched retention criterion.

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
        1D floating-point array, largest ratio of gap size to dropped rank
        within each gap.

    Notes
    -----
    - The number of gap sizes returned is always len(retained_ranks) + 1.
    - Rank 0 is corrected as rank 1, to prevent division by zero.

    See Also
    --------
    calc_gap_bounds : Calculate gap bounds for retained ranks and num
    ingests.
    """
    gap_bounds = calc_gap_bounds(retained_ranks, num_ingests)
    gap_sizes = calc_gap_sizes_from_gap_bounds(gap_bounds)

    return _calc_stretched_ratios_from_gaps(gap_bounds, gap_sizes)
