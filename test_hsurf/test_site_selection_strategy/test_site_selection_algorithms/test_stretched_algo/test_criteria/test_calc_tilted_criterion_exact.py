import pytest

from hsurf.hsurf import stretched_algo as algo


@pytest.mark.parametrize(
    "surface_size, num_depositions, expected_criterion_value",
    [
        (8, 0, 0),
        (8, 1, 0),
        (8, 8, 0),
        (8, 9, 0.5),
    ],
)
def test_calc_tilted_criterion_exact(
    surface_size: int,
    num_depositions: int,
    expected_criterion_value: int,
):
    assert (
        algo.calc_tilted_criterion_exact(surface_size, num_depositions)
        == expected_criterion_value
    )
