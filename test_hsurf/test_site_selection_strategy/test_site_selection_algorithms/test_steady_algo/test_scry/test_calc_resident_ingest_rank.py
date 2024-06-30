import itertools as it
import typing

import pytest

from hsurf.hsurf import steady_algo as algo


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
def test_calc_resident_ingest_rank_integration(
    surface_size: int,
    num_generations_bidder: typing.Callable,
):
    num_generations = num_generations_bidder(surface_size)
    surface_ingest_ranks = [0] * surface_size
    for rank in range(num_generations):
        for site, actual_ingest_rank in enumerate(surface_ingest_ranks):
            calculated_ingest_rank = algo.calc_resident_ingest_rank(
                site,
                surface_size,
                rank,
            )
            assert calculated_ingest_rank == actual_ingest_rank, {
                "actual ingest rank": actual_ingest_rank,
                "calculated ingest rank": calculated_ingest_rank,
                "num ingests": rank,
                "rank": rank,
                "site": site,
            }

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
        surface_ingest_ranks[target_site] = rank
