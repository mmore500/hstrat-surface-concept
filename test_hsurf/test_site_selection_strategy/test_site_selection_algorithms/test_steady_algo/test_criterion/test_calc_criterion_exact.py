import pytest

from hsurf.hsurf import steady_algo as algo


@pytest.mark.parametrize(
    "surface_size, num_depositions, expected_criterion_value",
    [
        (8, 0, 0),
        (8, 1, 0),
        (8, 8, 0),
        (8, 9, 1),
        (8, 500, 126),
        (8, 15, 2),
        (8, 16, 2),
        (8, 17, 3),
        (64, 0, 0),
        (64, 1, 0),
        (64, 8, 0),
        (64, 64, 0),
        (64, 65, 1),
        (64, 1024, 30),
        (64, 1100, 31),
        (64, 4000, 63),
    ],
)
def test_calc_criterion_exact(
    surface_size: int,
    num_depositions: int,
    expected_criterion_value: int,
):
    assert (
        algo.calc_criterion_exact(surface_size, num_depositions)
        == expected_criterion_value
    )
