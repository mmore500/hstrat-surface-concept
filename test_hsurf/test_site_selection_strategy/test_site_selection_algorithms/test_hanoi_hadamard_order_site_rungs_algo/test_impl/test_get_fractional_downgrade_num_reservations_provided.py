import itertools as it

import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.hanoi_hadamard_order_site_rungs_algo._impl import (
    get_fractional_downgrade_num_reservations_provided,
    get_fractional_downgrade_state,
    get_num_incidence_reservations_at_rank,
    get_surface_rank_capacity,
)


@pytest.mark.parametrize("hanoi_value", range(4))
@pytest.mark.parametrize("surface_size", [8, 32, 128])
@pytest.mark.parametrize("rank", range(0, 255, 12))
def test_get_fractional_downgrade_num_reservations_provided_smoke(
    hanoi_value: int, surface_size: int, rank: int
):
    # just a smoke test
    fractional_downgrade_state = get_fractional_downgrade_state(
        hanoi_value, surface_size, rank
    )
    if fractional_downgrade_state is not None:
        actual_result = get_fractional_downgrade_num_reservations_provided(
            hanoi_value, surface_size, rank, fractional_downgrade_state
        )
        assert isinstance(actual_result, int)


@pytest.mark.parametrize("surface_size", [8, 32, 128])
def test_get_fractional_downgrade_num_reservations_provided_range(
    surface_size: int,
):
    max_rank = min(1000, get_surface_rank_capacity(surface_size))
    for hanoi_value, rank in it.product(range(surface_size), range(max_rank)):
        fractional_downgrade_state = get_fractional_downgrade_state(
            hanoi_value, surface_size, rank
        )
        if fractional_downgrade_state is None:
            continue
        actual_result = get_fractional_downgrade_num_reservations_provided(
            hanoi_value, surface_size, rank, fractional_downgrade_state
        )
        assert isinstance(actual_result, int)
        baseline = get_num_incidence_reservations_at_rank(rank, surface_size)
        assert baseline // 2 <= actual_result <= baseline * 2
        assert 0 < actual_result <= surface_size
