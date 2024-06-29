from ....site_selection_bounds import calc_gap_size_lower_bound


def calc_criterion_lower_bound(
    surface_size: int, num_depositions: int
) -> float:
    return calc_gap_size_lower_bound(surface_size, num_depositions)
