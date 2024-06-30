import numpy as np
import pytest

from hsurf.hsurf import steady_algo as algo


@pytest.mark.parametrize(
    "surface_size",
    [2**i for i in range(1, 10)],
)
@pytest.mark.parametrize(
    "num_depositions",
    [0, 1, 63, 64, 65, 80, 100, 1000, 1023, 1024, 1025],
)
def test_calc_steady_criterion_upper_bound(
    surface_size: int,
    num_depositions: int,
):
    assert (
        algo.calc_steady_criterion_exact(surface_size, num_depositions)
        <= algo.calc_steady_criterion_upper_bound(surface_size, num_depositions)
        <= num_depositions
    )


@pytest.mark.parametrize(
    "num_depositions",
    np.random.RandomState(seed=1).randint(0, 2**32, 1000),
)
def test_calc_steady_criterion_upper_bound_large(num_depositions: int):
    surface_size = 32
    if num_depositions >= surface_size**2:
        return
    assert (
        algo.calc_steady_criterion_exact(surface_size, num_depositions)
        <= algo.calc_steady_criterion_upper_bound(surface_size, num_depositions)
        <= num_depositions
    )
