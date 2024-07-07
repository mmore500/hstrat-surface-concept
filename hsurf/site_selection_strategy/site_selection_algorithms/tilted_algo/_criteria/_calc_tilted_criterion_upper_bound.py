from .._impl._get_global_epoch import (
    _get_global_shifted_epoch,
    _get_global_shifted_mini_epoch,
)


def calc_tilted_criterion_upper_bound(
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

    tight_exp = -min(
        meta_epoch - (surface_size.bit_length() - 1) + 1,
        0,
    )
    tight_bound = 1 / (2**tight_exp - 0.5)

    approx_inverse1 = max(
        0.5 * surface_size / (mini_epoch + surface_size.bit_length()),
        1,
    )
    approx_bound1 = 1 / (approx_inverse1 - 0.5)

    approx_inverse2 = max(
        0.25 * surface_size / mini_epoch,
        1,
    )
    approx_bound2 = 1 / (approx_inverse2 - 0.5)

    return min(  # return tightest bound
        tight_bound,
        approx_bound1,
        approx_bound2,
    )
