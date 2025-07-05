from .....pylib import bit_floor
from ....site_selection_bounds import calc_gap_size_lower_bound


def calc_steady_criterion_upper_bound(
    surface_size: int, num_ingests: int
) -> float:
    assert surface_size > 0
    assert num_ingests >= 0
    if num_ingests < surface_size:
        return 0

    res = 2 * bit_floor(num_ingests // surface_size) - 1

    assert (
        res
        <= (2 * (surface_size + 1) / surface_size)
        * calc_gap_size_lower_bound(surface_size, num_ingests)
        + 1
    )

    return res
