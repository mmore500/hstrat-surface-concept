import pytest

from hsurf.hsurf import tilted_hadamard_order_site_rungs_algo as algo
from hsurf.pylib import longevity_ordering_descending as hadamard_order
from hsurf.pylib import site_selection_eval


@pytest.mark.parametrize("surface_size", [8, 32, 128])
@pytest.mark.parametrize("rank", range(0, 255, 12))
def test_pick_ingest_site_smoke(surface_size: int, rank: int) -> int:
    # just a smoke test
    ingest_site = algo.pick_ingest_site(rank, surface_size)
    assert isinstance(ingest_site, int)
    assert 0 <= ingest_site < surface_size


@pytest.mark.parametrize("surface_size", [2**exp for exp in range(2, 12)])
@pytest.mark.parametrize(
    "max_generations",
    [2**10, pytest.param(2**18, marks=pytest.mark.heavy)],
)
def test_pick_ingest_site_hanoi_value_overwrite_order(
    surface_size: int,
    max_generations: int,
):
    res = site_selection_eval.get_first_decreasing_hanoi_value_ingest(
        algo.pick_ingest_site,
        surface_size=surface_size,
        num_generations=min(
            max_generations,
            algo._impl.get_surface_rank_capacity(surface_size) - 1,
        ),
    )
    assert res is None, str(res)


@pytest.mark.parametrize("surface_size", [2**exp for exp in range(2, 12)])
@pytest.mark.parametrize(
    "max_generations",
    [2**10, pytest.param(2**18, marks=pytest.mark.heavy)],
)
def test_pick_ingest_site_incidence_reservation_drop_order(
    surface_size: int, max_generations: int
):
    res = site_selection_eval.get_first_ingest_over_too_new_site(
        algo.pick_ingest_site,
        algo._impl.get_num_reservations_provided,
        hadamard_order.get_longevity_mapped_position_of_index,
        surface_size=surface_size,
        num_generations=min(
            max_generations,
            algo._impl.get_surface_rank_capacity(surface_size) - 1,
        ),
    )
    assert res is None, str(res)
