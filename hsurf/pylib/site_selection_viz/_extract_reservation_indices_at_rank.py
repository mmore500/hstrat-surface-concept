import itertools as it
import typing

import pandas as pd


def extract_reservation_indices_at_rank(
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
