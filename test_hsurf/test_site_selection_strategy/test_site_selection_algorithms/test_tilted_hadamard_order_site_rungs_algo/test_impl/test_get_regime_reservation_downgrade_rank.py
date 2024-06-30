import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._impl import (
    get_regime_reservation_downgrade_rank,
)


@pytest.mark.parametrize("hanoi_value", range(4))
@pytest.mark.parametrize("surface_size", [8, 32, 128])
@pytest.mark.parametrize("rank", range(0, 255, 12))
def test_get_regime_reservation_downgrade_rank(
    hanoi_value: int, surface_size: int, rank: int
):
    # just a smoke test
    actual_result = get_regime_reservation_downgrade_rank(
        hanoi_value, surface_size, rank
    )
    assert isinstance(actual_result, int)
