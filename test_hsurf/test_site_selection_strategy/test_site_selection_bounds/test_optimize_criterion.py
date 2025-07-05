import pytest

from hsurf.site_selection_strategy.site_selection_bounds import (
    calc_gap_size_lower_bound,
    optimize_criterion,
)


@pytest.mark.parametrize("surface_size", range(1, 10))
@pytest.mark.parametrize("num_ingests", range(100))
def test_optimize_criterion(surface_size: int, num_ingests: int):
    assert optimize_criterion(
        surface_size, num_ingests, lambda a, b: b - a - 1
    ) == calc_gap_size_lower_bound(surface_size, num_ingests)
