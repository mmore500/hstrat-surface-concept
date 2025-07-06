from ....site_selection_bounds import calc_stretched_ratio_lower_bound


def calc_stretched_criterion_lower_bound(
    surface_size: int, num_ingests: int
) -> float:
    return calc_stretched_ratio_lower_bound(surface_size, num_ingests)
