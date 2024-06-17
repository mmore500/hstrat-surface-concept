import pytest

from hsurf.pylib import hanoi
from hsurf.pylib.site_selection_eval import make_surface_history_df
from hsurf.site_selection_strategy.site_selection_algorithms.stretched_algo import (
    pick_deposition_site,
)
from hsurf.site_selection_strategy.site_selection_algorithms.tilted_algo._impl import (
    get_hanoi_num_reservations,
)

expected8 = [
    0,  # 0:0
    1,  # 1:1
    5,  # 2:0
    2,  # 3:2
    4,  # 4:0
    6,  # 5:1
    7,  # 6:0
    3,  # 7:3
]


def test_pick_deposition_site8():
    surface_size = 8
    for rank in range(len(expected8)):
        assert pick_deposition_site(rank, surface_size) == expected8[rank]


expected16 = [
    0,  # 0:0
    1,  # 1:1
    9,  # 2:0
    2,  # 3:2
    6,  # 4:0
    10,  # 5:1
    13,  # 6:0
    3,  # 7:3
    5,  # 8:0
    7,  # 9:1
    8,  # 10:0
    11,  # 11:2
    12,  # 12:0
    14,  # 13:1
    15,  # 14:0
    4,  # 15:4
]


def test_pick_deposition_site16():
    surface_size = 16
    for rank in range(len(expected16)):
        assert pick_deposition_site(rank, surface_size) == expected16[rank]


@pytest.mark.parametrize(
    "surface_size, num_generations",
    [
        (8, 127),
        (16, 2**12),
        (32, 2**12),
        (64, 2**12),
    ],
)
def test_layering(surface_size: int, num_generations: int):
    df = make_surface_history_df(
        pick_deposition_site, surface_size, num_generations
    )

    for (hanoi_value, rank), group in df.groupby(
        [
            "hanoi value",
            "rank",
        ],
    ):
        hanoi_value, rank = int(hanoi_value), int(rank)  # pure python ints
        if rank == -1:
            continue
        if hanoi_value == -1:
            continue
        assert hanoi_value >= 0 and rank >= 0

        count = hanoi.get_incidence_count_of_hanoi_value_through_index(
            hanoi_value, rank
        )
        assert count >= 1
        num_reservations = min(
            get_hanoi_num_reservations(rank + 1, surface_size),
            get_hanoi_num_reservations(rank, surface_size),
        )
        assert num_reservations >= 1
        target_count = min(count, num_reservations)
        # should have expected hanoi population
        assert len(group) >= target_count  # may be larger if not yet eliminated

        incidences = {
            hanoi.get_hanoi_value_incidence_at_index(rank)
            for rank in group["deposition rank"]
        }
        # should always have first n // 2 incidences
        for lookup in range((len(incidences) + 1) // 2):
            assert lookup in incidences
