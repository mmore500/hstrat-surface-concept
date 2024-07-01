from ...tilted_algo._impl._get_global_epoch import (
    _get_global_shifted_epoch,
    _get_global_shifted_mini_epoch,
)


def calc_stretched_criterion_upper_bound(
    surface_size: int, num_ingests: int
) -> float:
    assert surface_size > 0
    assert num_ingests >= 0
    if num_ingests <= surface_size:
        return 0

    assert num_ingests
    rank = num_ingests - 1
    mini_epoch = _get_global_shifted_mini_epoch(rank, surface_size)
    meta_epoch = _get_global_shifted_epoch(rank, surface_size)

    exp = min(
        meta_epoch - (surface_size.bit_length() - 1) + 1,
        0,  # correction for last epoch of tight bound
    )
    return min(
        2**exp,  # tight bound
        # ... approximate bounds
        2 * (mini_epoch + surface_size.bit_length()) / surface_size,
        4 * mini_epoch / surface_size,
    )
