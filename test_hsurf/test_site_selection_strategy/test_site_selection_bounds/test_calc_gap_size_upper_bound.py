import pytest

from hsurf.site_selection_strategy.site_selection_bounds import (
    calc_gap_size_upper_bound,
)


@pytest.mark.parametrize(
    "surface_size, num_ingests, expected",
    [
        (1, 0, 0),
        (10, 0, 0),
        (1, 1, 1),
        (10, 1, 1),
        (10, 10, 10),
        (10, 11, 11),
        (1, 11, 11),
        (5, 26, 26),
        (5, 25, 25),
        (20, 100, 100),
        (20, 101, 101),
    ],
)
def test_calc_gap_size_upper_bound(surface_size, num_ingests, expected):
    assert calc_gap_size_upper_bound(surface_size, num_ingests) == expected
