import itertools as it
import typing

import pytest

from hsurf.hsurf import stretched_try_algo as algo
from hsurf.pylib import hanoi
from hsurf.site_selection_strategy.site_selection_algorithms.tilted_algo._impl import (
    get_site_genesis_reservation_index_physical,
)


@pytest.mark.parametrize(
    "surface_size",
    [2**x for x in range(3, 10)]
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
    hanoi_values = [0] * surface_size
    surface_ingest_ranks = [0] * surface_size

    for rank in range(num_generations):
        for site, actual_ingest_rank in enumerate(surface_ingest_ranks):
            calculated_ingest_rank = algo.calc_resident_ingest_rank(
                site,
                surface_size,
                rank,
                grip=get_grip(site, surface_size),
            )
            assert calculated_ingest_rank == actual_ingest_rank, str(
                {
                    "rank": rank,
                    "site": site,
                    "actual": actual_ingest_rank,
                    "calculated": calculated_ingest_rank,
                    "val": surface_ingest_ranks,
                    "hv": hanoi_values,
                },
            )

        assert all(
            it.starmap(
                int.__eq__,
                zip(
                    [*algo.iter_resident_ingest_ranks(surface_size, rank)],
                    surface_ingest_ranks,
                    strict=True,
                ),
            )
        )

        # update surface
        target_site = algo.pick_ingest_site(rank, surface_size)
        if target_site != surface_size:
            surface_ingest_ranks[target_site] = rank
            hanoi_values[target_site] = hanoi.get_hanoi_value_at_index(rank)
