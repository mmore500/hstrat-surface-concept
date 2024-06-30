import numpy as np


def calc_gap_ratio_lower_bound(
    surface_size: int, num_ingests: int
) -> float:
    """Calculate the lower bound on ratio of gap size to dropped data item rank.

    Parameters
    ----------
    surface_size : int
        The maximum number of items that can be retained.
    num_ingests : int
        The current position or time step.

        Must be non-negative and less than or equal to `2**surface_size`.

    Returns
    -------
    float
        The calculated lower bound of the gap size ratio.

    Notes
    -----
    - Rank 0 is corrected as rank 1, to prevent division by zero.
    """
    assert num_ingests <= 2**surface_size
    assert surface_size

    num_discarded = max(num_ingests - surface_size, 0)
    if num_discarded == 0:
        return 0

    rank = num_ingests - 1
    if rank == 1:
        return 1

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
    return 1 / (num_ingests - num_gaps - num_discarded)
