from ....site_selection_bounds import calc_tilted_ratio_upper_bound


def calc_tilted_criterion_upper_bound(
    surface_size: int, num_ingests: int
) -> float:
    return calc_tilted_ratio_upper_bound(surface_size, num_ingests)
