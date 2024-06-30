from ....site_selection_criteria import calc_stretched_ratios
from .._scry import iter_retained_ingest_ranks


def calc_stretched_criterion_exact(
    surface_size: int, num_ingests: int
) -> float:
    assert surface_size > 0
    assert num_ingests >= 0

    gap_ratios = calc_stretched_ratios(
        [*iter_retained_ingest_ranks(surface_size, num_ingests)],
        num_ingests,
    )
    assert len(gap_ratios)
    return gap_ratios.max()
