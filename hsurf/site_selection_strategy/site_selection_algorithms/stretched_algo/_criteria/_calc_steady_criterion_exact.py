from ....site_selection_criteria import calc_gap_sizes
from .._iter_retained_ingest_ranks import iter_retained_ingest_ranks


def calc_steady_criterion_exact(
    surface_size: int, num_ingests: int
) -> float:
    assert surface_size > 0
    assert num_ingests >= 0

    gap_sizes = calc_gap_sizes(
        [*iter_retained_ingest_ranks(surface_size, num_ingests)],
        num_ingests,
    )
    assert len(gap_sizes)
    return gap_sizes.max()
