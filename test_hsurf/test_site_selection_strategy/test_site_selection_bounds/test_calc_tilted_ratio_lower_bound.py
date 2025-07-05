from hsurf.site_selection_strategy.site_selection_bounds import (
    calc_tilted_ratio_lower_bound,
)


def test_calc_tilted_ratio_lower_bound_smoke():
    assert 0 <= calc_tilted_ratio_lower_bound(100, 64) <= 1
