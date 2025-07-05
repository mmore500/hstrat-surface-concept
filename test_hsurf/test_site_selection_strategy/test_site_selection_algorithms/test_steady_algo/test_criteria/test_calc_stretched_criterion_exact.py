import pytest

from hsurf.hsurf import steady_algo as algo


@pytest.mark.parametrize(
    "surface_size, num_ingests, expected_criterion_value",
    [
        (8, 0, 0),
        (8, 1, 0),
        (8, 8, 0),
        (8, 9, 0.25),
        (8, 10, 0.25),
    ],
)
def test_calc_stretched_criterion_exact(
    surface_size: int,
    num_ingests: int,
    expected_criterion_value: int,
):
    assert (
        algo.calc_stretched_criterion_exact(surface_size, num_ingests)
        == expected_criterion_value
    )
