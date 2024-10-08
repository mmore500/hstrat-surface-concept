import pytest

from hsurf.hsurf import steady_try_full_algo as algo
from hsurf.site_selection_strategy.site_selection_bounds import (
    calc_gap_size_lower_bound as ideal_lb,
)


@pytest.mark.parametrize(
    "surface_size",
    [2**i for i in range(1, 10)],
)
@pytest.mark.parametrize(
    "num_ingests",
    [0, 1, 63, 64, 65, 80, 100, 1000, 1023, 1024, 1025],
)
def test_calc_steady_criterion_lower_bound(
    surface_size: int,
    num_ingests: int,
):
    assert (
        ideal_lb(surface_size, num_ingests)
        <= algo.calc_steady_criterion_lower_bound(surface_size, num_ingests)
        <= algo.calc_steady_criterion_exact(surface_size, num_ingests)
    )
