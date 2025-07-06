from ....site_selection_bounds import calc_tilted_ratio_upper_bound


def calc_tilted_criterion_upper_bound(
    surface_size: int, num_ingests: int
) -> float:
    # why isn't it 4x tilted_algo bound?
    # 8x fails too...
    # leave as worst case for now
    return calc_tilted_ratio_upper_bound(surface_size, num_ingests)
