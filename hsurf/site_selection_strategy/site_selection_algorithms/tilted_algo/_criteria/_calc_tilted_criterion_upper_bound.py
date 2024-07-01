from .._impl._get_global_epoch import _get_global_shifted_epoch


def calc_tilted_criterion_upper_bound(
    surface_size: int, num_ingests: int
) -> float:
    assert surface_size > 0
    assert num_ingests >= 0
    if num_ingests <= surface_size:
        return 0

    assert num_ingests
    rank = num_ingests - 1
    meta_epoch = _get_global_shifted_epoch(rank, surface_size)

    exp = -min(
        meta_epoch - (surface_size.bit_length() - 1) + 1,
        0,
    )
    return 1 / (2**exp - 0.5)
