import numpy as np

from ._calc_gap_sizes import calc_gap_sizes_from_gap_bounds
from ._impl import calc_gap_bounds


def calc_stretched_ratios(
    retained_ranks: np.array, current_rank: int
) -> np.array:
    """Calculate statistic for stretched retention criterion.

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
        1D floating-point array, largest ratio of gap size to dropped rank
        within each gap.

    Notes
    -----
    - If retained_ranks is empty, returns an empty array.
    - Otherwise, the number of gap sizes returned is always len(retained_ranks)
      + 1.
    - Rank 0 is corrected as rank 1, to prevent division by zero.

    See Also
    --------
    calc_gap_bounds : Calculate gap bounds for retained ranks and current rank.
    """
    if retained_ranks.size == 0:
        return np.array([], dtype=int)

    gap_bounds = calc_gap_bounds(retained_ranks, current_rank)
    gap_sizes = calc_gap_sizes_from_gap_bounds(gap_bounds)

    return gap_sizes / np.maximum(gap_bounds[:-1] + 1, 1)
