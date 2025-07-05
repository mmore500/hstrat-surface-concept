import pytest

from hsurf.hsurf import steady_try_algo as algo


@pytest.mark.parametrize(
    "surface_size, num_ingests, expected_criterion_value",
    [
        (8, 0, 0),
        (8, 1, 0),
        (8, 8, 0),
        (8, 9, 1),
        (8, 500, 63),
        (8, 15, 1),
        (8, 16, 2),
        (8, 17, 2),
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
def test_calc_steady_criterion_exact(
    surface_size: int,
    num_ingests: int,
    expected_criterion_value: int,
):
    assert (
        algo.calc_steady_criterion_exact(surface_size, num_ingests)
        == expected_criterion_value
    )
