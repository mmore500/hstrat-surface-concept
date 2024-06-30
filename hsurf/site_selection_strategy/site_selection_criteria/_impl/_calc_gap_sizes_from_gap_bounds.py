import numpy as np


def calc_gap_sizes_from_gap_bounds(gap_bounds: np.array) -> np.array:
    """
    Calculate gap sizes from gap bounds.

    Parameters
    ----------
    gap_bounds : np.ndarray
        1D array of integer gap bounds.

    Returns
    -------
    np.ndarray
        1D array of integer gap sizes.

    See Also
    --------
    calc_gap_bounds : Calculate gap bounds for retained ranks and num
    ingests.
    """
    if len(gap_bounds) == 0:
        return np.array([], dtype=int)

    gap_sizes = np.diff(gap_bounds) - 1
    assert (gap_sizes >= 0).all()
    return gap_sizes
