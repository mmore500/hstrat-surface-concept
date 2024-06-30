import pytest

from hsurf.hsurf import tilted_sticky_algo as algo
from hsurf.site_selection_strategy.site_selection_bounds import (
    calc_tilted_ratio_lower_bound as ideal_lb,
)


@pytest.mark.parametrize(
    "surface_size",
    [2**i for i in range(1, 10)],
)
@pytest.mark.parametrize(
    "num_depositions",
    [0, 1, 63, 64, 65, 80, 100, 1000, 1023, 1024, 1025],
)
def test_calc_tilted_criterion_lower_bound(
    surface_size: int,
    num_depositions: int,
):
    if num_depositions >= surface_size**2:
        return
    assert (
        ideal_lb(surface_size, num_depositions)
        <= algo.calc_tilted_criterion_lower_bound(surface_size, num_depositions)
        <= algo.calc_tilted_criterion_exact(surface_size, num_depositions)
    )
