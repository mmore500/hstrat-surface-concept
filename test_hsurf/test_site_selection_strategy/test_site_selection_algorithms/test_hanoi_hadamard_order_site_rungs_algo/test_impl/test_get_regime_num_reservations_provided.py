import itertools as it

import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._impl import (
    get_num_incidence_reservations_at_rank,
    get_regime_num_reservations_provided,
    get_surface_rank_capacity,
)


@pytest.mark.parametrize("hanoi_value", range(4))
@pytest.mark.parametrize("surface_size", [8, 32, 128])
@pytest.mark.parametrize("rank", range(0, 255, 12))
def test_get_regime_num_reservations_provided_smoke(
    hanoi_value: int, surface_size: int, rank: int
):
    # just a smoke test
    actual_result = get_regime_num_reservations_provided(
        hanoi_value, surface_size, rank
    )
    assert isinstance(actual_result, int)


@pytest.mark.parametrize("surface_size", [8, 32, 128])
def test_get_regime_num_reservations_provided_range(surface_size: int):
    max_rank = min(1000, get_surface_rank_capacity(surface_size))
    for hanoi_value, rank in it.product(range(surface_size), range(max_rank)):
        actual_result = get_regime_num_reservations_provided(
            hanoi_value, surface_size, rank,
        )
        baseline = get_num_incidence_reservations_at_rank(rank, surface_size)
        assert baseline // 2 <= actual_result <= baseline * 2
        assert 0 < actual_result <= surface_size
