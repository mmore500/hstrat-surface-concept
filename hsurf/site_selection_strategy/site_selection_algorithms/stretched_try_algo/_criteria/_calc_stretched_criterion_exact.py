from ....site_selection_criteria import calc_stretched_ratios
from .._iter_retained_deposition_ranks import iter_retained_deposition_ranks


def calc_stretched_criterion_exact(
    surface_size: int, num_depositions: int
) -> float:
    assert surface_size > 0
    assert num_depositions >= 0

    gap_ratios = calc_stretched_ratios(
        [*iter_retained_deposition_ranks(surface_size, num_depositions)],
        num_depositions,
    )
    assert len(gap_ratios)
    return gap_ratios.max()
