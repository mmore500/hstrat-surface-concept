import numpy as np
import pytest

from hsurf.hsurf import stretched_try_algo as algo


@pytest.mark.parametrize(
    "surface_size",
    [2**i for i in range(1, 10)],
)
@pytest.mark.parametrize(
    "num_ingests",
    [0, 1, 63, 64, 65, 80, 100, 1000, 1023, 1024, 1025],
)
def test_calc_steady_criterion_upper_bound(
    surface_size: int,
    num_ingests: int,
):
    if num_ingests >= surface_size**2:
        return
    assert (
        algo.calc_steady_criterion_exact(surface_size, num_ingests)
        <= algo.calc_steady_criterion_upper_bound(surface_size, num_ingests)
        <= num_ingests
    )


@pytest.mark.parametrize(
    "num_ingests",
    np.random.RandomState(seed=1).randint(0, 2**32, 1000),
)
def test_calc_steady_criterion_upper_bound_large(num_ingests: int):
    surface_size = 32
    if num_ingests >= surface_size**2:
        return
    assert (
        algo.calc_steady_criterion_exact(surface_size, num_ingests)
        <= algo.calc_steady_criterion_upper_bound(surface_size, num_ingests)
        <= num_ingests
    )
