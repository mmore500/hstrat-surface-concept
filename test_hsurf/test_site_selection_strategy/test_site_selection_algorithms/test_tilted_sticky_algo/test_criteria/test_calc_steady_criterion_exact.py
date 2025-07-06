import pytest

from hsurf.hsurf import tilted_sticky_algo as algo


@pytest.mark.parametrize(
    "surface_size, num_ingests, expected_criterion_value",
    [
        (8, 0, 0),
        (8, 1, 0),
        (8, 8, 0),
        (8, 9, 1),
    ],
)
def test_calc_steady_criterion_exact(
    surface_size: int,
    num_ingests: int,
    expected_criterion_value: int,
):
    if num_ingests >= surface_size**2:
        return
    assert (
        algo.calc_steady_criterion_exact(surface_size, num_ingests)
        == expected_criterion_value
    )
