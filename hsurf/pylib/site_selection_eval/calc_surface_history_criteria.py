import typing

import numpy as np
import pandas as pd


def calc_surface_history_criteria(
    surface_history_df: pd.DataFrame,
    progress_wrap: typing.Callable = lambda x: x,
) -> pd.DataFrame:

    surface_size = surface_history_df["site"].max() + 1

    records = []
    for rank, group_df in progress_wrap(
        surface_history_df[surface_history_df["deposition rank"] != -1].groupby(
            "rank"
        ),
    ):
        deposition_ranks = sorted(group_df["deposition rank"])
        gap_bounds = np.array([-1, *deposition_ranks, rank + 1])
        gap_sizes = np.diff(gap_bounds) - 1
        assert (gap_sizes >= 0).all()

        gap_lowest_ranks = gap_bounds[:-1] + 1
        gap_stretched_ratios = gap_sizes / np.maximum(gap_lowest_ranks, 1)

        gap_highest_ranks = gap_bounds[1:] - 1
        gap_tilted_ratios = gap_sizes / np.maximum(rank - gap_highest_ranks, 1)

        # TODO add assertions for consistency
        # between ideal, worst, and upper bound
        records.append(
            {
                "rank": rank,
                "steady criterion": gap_sizes.max(),
                "stretched criterion": gap_stretched_ratios.max(),
                "tilted criterion": gap_tilted_ratios.max(),
                "kind": "worst",
            },
        )
        weights = gap_sizes if gap_sizes.any() else None
        records.append(
            {
                "rank": rank,
                "steady criterion": np.average(gap_sizes, weights=weights),
                "stretched criterion": np.average(
                    gap_stretched_ratios, weights=weights
                ),
                "tilted criterion": np.average(
                    gap_tilted_ratios, weights=weights
                ),
                "kind": "mean",
            },
        )
        gap_ratio_ideal = max(
            np.floor(rank ** (1 / (surface_size - 1)) - 1),
            0,
        )
        records.append(
            {
                "rank": rank,
                "steady criterion": rank // surface_size,
                "stretched criterion": gap_ratio_ideal,
                "tilted criterion": gap_ratio_ideal,
                "kind": "ideal",
            },
        )
        gap_ratio_upper_bound = np.nan
        records.append(
            {
                "rank": rank,
                "steady criterion": 2 * np.ceil(rank / surface_size),
                "stretched criterion": gap_ratio_upper_bound,
                "tilted criterion": gap_ratio_upper_bound,
                "kind": "upper bound",
            },
        )

    return pd.DataFrame.from_records(records)
