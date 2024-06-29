import pytest

from hsurf.site_selection_strategy.site_selection_bounds import (
    calc_gap_size_lower_bound,
)


@pytest.mark.parametrize(
    "surface_size, num_depositions, expected",
    [
        (1, 0, 0),
        (10, 0, 0),
        (1, 1, 0),
        (10, 1, 0),
        (10, 10, 0),
        (10, 11, 1),
        (1, 11, 5),
        (5, 26, 4),
        (5, 25, 4),
        (20, 100, 4),
        (20, 101, 4),
    ],
)
def test_calc_gap_size_lower_bound(surface_size, num_depositions, expected):
    assert calc_gap_size_lower_bound(surface_size, num_depositions) == expected
