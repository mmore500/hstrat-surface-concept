from ....site_selection_bounds import calc_gap_size_lower_bound


def calc_steady_criterion_lower_bound(
    surface_size: int, num_ingests: int
) -> float:
    return calc_gap_size_lower_bound(surface_size, num_ingests)
