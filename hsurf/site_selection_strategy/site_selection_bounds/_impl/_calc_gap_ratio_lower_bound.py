import numpy as np


def calc_gap_ratio_lower_bound(rank: int, surface_size: int) -> float:
    """Calculate the lower bound on ratio of gap size to dropped data item rank.

    Parameters
    ----------
    rank : int
        The current position or time step.

        Must be non-negative and less than `2**surface_size`.
    surface_size : int
        The maximum number of items that can be retained.

    Returns
    -------
    float
        The calculated lower bound of the gap size ratio.

    Notes
    -----
    - Rank 0 is corrected as rank 1, to prevent division by zero.
    """
    assert rank < 2**surface_size
    assert surface_size

    if rank < surface_size or rank == 1:
        return 0

    num_discarded = (rank + 1) - surface_size
    if num_discarded == 0:
        return 0

    num_gaps = np.floor(
        surface_size
        * (
            np.log(num_discarded * (rank ** (1 / surface_size) - 1) + 1)
            / np.log(rank)
        )
        - 1
    )

    # this doesn't work...
    # last_gap_size = np.floor(rank ** (num_gaps / surface_size))
    # gap_ratio_ideal = last_gap_size / (rank - last_gap_size + 1)

    # ... but this works
    # note that smallest gap size will always be 0 or 1
    return 1 / (rank - num_gaps - num_discarded + 1)
