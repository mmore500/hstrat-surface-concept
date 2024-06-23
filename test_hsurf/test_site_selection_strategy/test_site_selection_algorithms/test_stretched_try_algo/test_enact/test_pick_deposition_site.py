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


@pytest.mark.parametrize(
    "rank, surface_size, expected_result",
    [
        (1, 8, 1),
        (2, 8, 5),
        (3, 8, 2),
        (4, 8, 4),
        (5, 8, 6),
        (6, 8, 7),
        (7, 8, 3),
        (8, 8, 7),
        (9, 8, 7),
        (10, 8, 7),
        (11, 8, 7),
        (12, 8, 4),
        (13, 8, 4),
        (14, 8, 4),
        (15, 8, 4),
        (16, 8, 5),
        (17, 8, 5),
        (18, 8, 5),
        (19, 8, 5),
        (20, 8, 5),
        (21, 8, 5),
        (22, 8, 5),
        (23, 8, 5),
        (24, 8, 5),
        (25, 8, 5),
        (26, 8, 5),
        (27, 8, 5),
        (28, 8, 5),
        (29, 8, 5),
        (30, 8, 5),
        (31, 8, 5),
        (32, 8, 6),
        (33, 8, 6),
        (34, 8, 6),
        (35, 8, 6),
        (36, 8, 6),
        (37, 8, 6),
        (38, 8, 6),
        (39, 8, 6),
        (40, 8, 6),
        (41, 8, 6),
        (42, 8, 6),
        (43, 8, 6),
        (44, 8, 6),
        (45, 8, 6),
        (46, 8, 6),
        (47, 8, 6),
        (48, 8, 6),
        (49, 8, 6),
        (50, 8, 6),
        (51, 8, 6),
        (52, 8, 6),
        (53, 8, 6),
        (54, 8, 6),
        (55, 8, 6),
        (56, 8, 6),
        (57, 8, 6),
        (58, 8, 6),
        (59, 8, 6),
        (60, 8, 6),
        (61, 8, 6),
        (62, 8, 6),
        (63, 8, 6),
        (64, 8, 7),
        (65, 8, 7),
        (66, 8, 7),
        (67, 8, 7),
        (68, 8, 7),
        (69, 8, 7),
        (70, 8, 7),
        (71, 8, 7),
        (72, 8, 7),
        (73, 8, 7),
        (74, 8, 7),
        (75, 8, 7),
        (76, 8, 7),
        (77, 8, 7),
        (78, 8, 7),
        (79, 8, 7),
        (80, 8, 7),
        (81, 8, 7),
        (82, 8, 7),
        (83, 8, 7),
        (84, 8, 7),
        (85, 8, 7),
        (86, 8, 7),
        (87, 8, 7),
        (88, 8, 7),
        (89, 8, 7),
        (90, 8, 7),
        (91, 8, 7),
        (92, 8, 7),
        (93, 8, 7),
        (94, 8, 7),
        (95, 8, 7),
        (96, 8, 7),
        (97, 8, 7),
        (98, 8, 7),
        (99, 8, 7),
        (37, 8, 6),
    ],
)
def test_pick_deposition_site_regression(
    rank: int,
    surface_size: int,
    expected_result: int,
):
    # for surface_size in 8, 32, 64, 1024:
    #     for rank in [
    #         *range(100),
    #         *map(
    #             int,
    #             np.random.RandomState(seed=1).randint(
    #                 0, 2 ** (surface_size), 10**2
    #             ),
    #         ),
    #     ]:
    #         result = pick_deposition_site(rank, surface_size)
    #         print(rank, surface_size, result)
    assert expected_result == pick_deposition_site(rank, surface_size)
