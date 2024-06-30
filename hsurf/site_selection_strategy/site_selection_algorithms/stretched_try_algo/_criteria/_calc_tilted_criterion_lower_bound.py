from ....site_selection_bounds import calc_tilted_ratio_lower_bound


def calc_tilted_criterion_lower_bound(
    surface_size: int, num_depositions: int
) -> float:
    return calc_tilted_ratio_lower_bound(surface_size, num_depositions)
