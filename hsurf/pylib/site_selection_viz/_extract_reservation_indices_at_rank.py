import itertools as it
import typing

import pandas as pd


def _steady_extract_reservation_indices_at_rank(
    surface_history_df: pd.DataFrame, rank: int
) -> typing.List[int]:
    surface_size = surface_history_df["site"].nunique()
    first_segment_size = surface_size.bit_length() - 1

    res = [0, 1]
    res.append(res[-1] + first_segment_size)
    for i in range(1, first_segment_size):
        num_bins = 2 ** (i - 1)
        bin_size = first_segment_size - i
        # segment_width = num_bins * bin_size
        # res.append(res[-1] + segment_width)
        for _ in range(num_bins):
            res.append(res[-1] + bin_size)

    assert res[-1] == surface_size
    return res[:-1]

def _steady_extract_reservation_indices_at_rank_(
    surface_history_df: pd.DataFrame, rank: int
) -> typing.List[int]:
    surface_size = surface_history_df["site"].nunique()
    first_segment_size = surface_size.bit_length() - 1

    res = [0]
    res.append(res[-1] + first_segment_size)
    for i in range(1, first_segment_size):
        num_bins = 2 ** (i - 1)
        bin_size = first_segment_size - i
        # segment_width = num_bins * bin_size
        # res.append(res[-1] + segment_width)
        for _ in range(num_bins):
            res.append(res[-1] + bin_size)

    assert res[-1] < surface_size
    return res

def _steady_full_extract_reservation_indices_at_rank(
    surface_history_df: pd.DataFrame, rank: int
) -> typing.List[int]:
    surface_size = surface_history_df["site"].nunique()
    first_segment_size = surface_size.bit_length()

    res = [0]
    res.append(res[-1] + first_segment_size)
    for i in range(1, first_segment_size - 1):
        num_bins = 2 ** (i - 1)
        bin_size = first_segment_size - 1 - i
        # segment_width = num_bins * bin_size
        # res.append(res[-1] + segment_width)
        for _ in range(num_bins):
            res.append(res[-1] + bin_size)

    assert res[-1] == surface_size
    return res[:-1]

def _tilted_extract_reservation_indices_at_rank(
    surface_history_df: pd.DataFrame, rank: int
) -> typing.List[int]:
    sorted_hanoi_values = (
        surface_history_df[surface_history_df["rank"] == rank]
        .sort_values("site", ascending=True)["hanoi value"]
        .to_list()
    )
    return [
        0,
        *(
            i + 1
            for i, (a, b) in enumerate(it.pairwise(sorted_hanoi_values))
            if a >= b
        ),
    ]


def extract_reservation_indices_at_rank(
    surface_history_df: pd.DataFrame, rank: int, reservation_mode: str
) -> typing.List[int]:
    return {
        "steady": _steady_extract_reservation_indices_at_rank,
        "steady_": _steady_extract_reservation_indices_at_rank_,
        "steady_full": _steady_full_extract_reservation_indices_at_rank,
        "tilted": _tilted_extract_reservation_indices_at_rank,
    }[reservation_mode](surface_history_df, rank)
