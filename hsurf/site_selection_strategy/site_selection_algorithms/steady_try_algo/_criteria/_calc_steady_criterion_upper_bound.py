import numpy as np


def calc_steady_criterion_upper_bound(
    surface_size: int, num_ingests: int
) -> float:
    assert surface_size > 0
    assert num_ingests >= 0
    if num_ingests < surface_size:
        return 0

    rank = num_ingests - 1
    assert rank
    return 2 * np.ceil(rank / surface_size)
