from ...stretched_try_algo._criteria import (
    calc_stretched_criterion_upper_bound as _impl,
)


def calc_stretched_criterion_upper_bound(
    surface_size: int, num_ingests: int
) -> float:
    return min(
        4 * _impl(surface_size, num_ingests),
        num_ingests,  # worst-possible bound
    )
