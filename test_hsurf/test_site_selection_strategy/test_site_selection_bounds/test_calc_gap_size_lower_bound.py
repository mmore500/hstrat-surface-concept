import pytest

from hsurf.site_selection_strategy.site_selection_bounds import (
    calc_gap_size_lower_bound,
)


@pytest.mark.parametrize(
    "rank, surface_size, expected",
    [
        (0, 1, 0),
        (0, 10, 0),
        (9, 10, 0),
        (10, 10, 1),
        (10, 1, 5),
        (25, 5, 4),
        (24, 5, 4),
        (100, 20, 4),
    ],
)
def test_calc_gap_size_lower_bound(rank, surface_size, expected):
    assert calc_gap_size_lower_bound(rank, surface_size) == expected
