import typing

import numpy as np


def optimize_criterion(
    surface_size: int,
    num_ingests: int,
    criterion: typing.Callable[[int, int], float],
) -> float:
    """Calculate the smallest-possible maximal value of a criterion function
    for any retention policy, given a rank and surface size.

    Parameters
    ----------
    surface_size : int
        The maximum number of items that can be retained.
    num_ingests : int
        The number of data items that have been ingested.
    criterion : callable
        A function that takes two item indices on either side of a gap, and
        returns a float.

    Returns
    -------
    float
        The minimized maximal criterion value.

    Notes
    -----
    This function uses dynamic programming to optimize the given criterion.
    """

    # dynamic programming array:
    # ------------> rank
    # |
    # |
    # |
    # V keep number
    num_keeps = min(num_ingests, surface_size)
    nrow = num_keeps
    ncol = num_ingests
    dp_array = np.zeros((nrow, ncol), dtype=float)
    for row in range(nrow):
        for col in range(ncol):
            if row == 0:
                dp_array[row, col] = criterion(-1, col)
            else:
                dp_array[row, col] = min(
                    (
                        max(criterion(from_, col), dp_array[row - 1, from_])
                        for from_ in range(col)
                    ),
                    default=0,
                )

    return min(
        (
            max(criterion(from_, num_ingests), dp_array[-1, from_])
            for from_ in range(ncol)
        ),
        default=0,
    )
