from ....site_selection_criteria import calc_tilted_ratios
from .._iter_retained_ingest_ranks import iter_retained_ingest_ranks


def calc_tilted_criterion_exact(
    surface_size: int, num_ingests: int
) -> float:
    assert surface_size > 0
    assert num_ingests >= 0

    gap_ratios = calc_tilted_ratios(
        [*iter_retained_ingest_ranks(surface_size, num_ingests)],
        num_ingests,
    )
    assert len(gap_ratios)
    return gap_ratios.max()
