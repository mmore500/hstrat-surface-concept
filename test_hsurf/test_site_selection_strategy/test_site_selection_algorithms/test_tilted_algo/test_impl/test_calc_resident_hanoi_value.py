import typing

import pytest

from hsurf.hsurf import tilted_algo as algo
from hsurf.pylib import hanoi
from hsurf.site_selection_strategy.site_selection_algorithms.tilted_algo._impl import (
    calc_resident_hanoi_value,
    get_site_genesis_reservation_index_physical,
)


@pytest.mark.parametrize(
    "surface_size",
    [2**x for x in range(1, 10)]
    + [pytest.param(2**x, marks=pytest.mark.heavy) for x in range(6, 11)],
)
@pytest.mark.parametrize(
    "num_generations_bidder",
    [
        lambda surface_size: 2**15 // surface_size,
        pytest.param(
            lambda surface_size: 2**18 // max(1, surface_size >> 9),
            marks=pytest.mark.heavy,
        ),
    ],
)
@pytest.mark.parametrize(
    "get_grip",
    [get_site_genesis_reservation_index_physical, lambda site, size: None],
)
def test_calc_resident_ingest_rank_integration(
    surface_size: int,
    num_generations_bidder: typing.Callable,
    get_grip: typing.Callable,
):
    num_generations = min(
        num_generations_bidder(surface_size),
        algo.get_ingest_capacity(surface_size),
    )
    surface_hanoi_values = [0] * surface_size
    surface_ingest_ranks = [0] * surface_size

    for rank in range(num_generations):
        for site, actual_hanoi_value in enumerate(surface_hanoi_values):
            calculated_hanoi_value = calc_resident_hanoi_value(
                site,
                surface_size,
                rank,
                grip=get_grip(site, surface_size),
            )
            assert calculated_hanoi_value == actual_hanoi_value, str(
                {
                    "rank": rank,
                    "site": site,
                    "actual": actual_hanoi_value,
                    "calculated": calculated_hanoi_value,
                    "ingest ranks": surface_ingest_ranks,
                    "hanoi values": surface_hanoi_values,
                },
            )

        # update surface
        target_site = algo.pick_ingest_site(rank, surface_size)
        surface_ingest_ranks[target_site] = rank
        surface_hanoi_values[target_site] = hanoi.get_hanoi_value_at_index(rank)
