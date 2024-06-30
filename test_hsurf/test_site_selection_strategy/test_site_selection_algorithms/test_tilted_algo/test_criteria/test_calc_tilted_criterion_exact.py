import pytest

from hsurf.hsurf import tilted_algo as algo


@pytest.mark.parametrize(
    "surface_size, num_depositions, expected_criterion_value",
    [
        (8, 0, 0),
        (8, 1, 0),
        (8, 8, 0),
        (8, 9, 1 / 8),
    ],
)
def test_calc_tilted_criterion_exact(
    surface_size: int,
    num_depositions: int,
    expected_criterion_value: int,
):
    if num_depositions >= surface_size**2:
        return
    assert (
        algo.calc_tilted_criterion_exact(surface_size, num_depositions)
        == expected_criterion_value
    )
