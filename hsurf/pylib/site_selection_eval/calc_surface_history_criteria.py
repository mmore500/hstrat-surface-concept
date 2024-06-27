import typing

import numpy as np
import pandas as pd


def calc_surface_history_criteria(
    surface_history_df: pd.DataFrame,
    progress_wrap: typing.Callable = lambda x: x,
    enforce_tilted_bound: bool = False,
    enforce_stretched_bound: bool = False,
) -> pd.DataFrame:

    surface_size = int(surface_history_df["site"].max() + 1)

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

        if rank > surface_size:
            num_discarded = rank - surface_size
            num_gaps = (
                surface_size
                * (
                    np.log(num_discarded * (rank ** (1 / surface_size) - 1) + 1)
                    / np.log(rank)
                )
                - 1
            )

            # doesn't work
            # last_gap_size = np.floor(rank ** (num_gaps / surface_size))
            # gap_ratio_ideal = last_gap_size / (rank - last_gap_size + 1)
            # works
            # note that smallest gap size will always be 0 or 1
            gap_ratio_ideal = 1 / (rank - num_gaps - num_discarded)
        else:
            gap_ratio_ideal = 0

        assert gap_ratio_ideal <= gap_stretched_ratios.max() or np.isclose(
            gap_ratio_ideal, gap_stretched_ratios.max()
        )
        assert gap_ratio_ideal <= gap_tilted_ratios.max() or np.isclose(
            gap_ratio_ideal, gap_tilted_ratios.max()
        )

        records.append(
            {
                "rank": rank,
                "steady criterion": rank // surface_size,
                "stretched criterion": gap_ratio_ideal,
                "tilted criterion": gap_ratio_ideal,
                "kind": "strict ideal",
            },
        )

        gap_ratio_naive = max(rank ** (1 / surface_size) - 1, 0)
        records.append(
            {
                "rank": rank,
                "steady criterion": rank / surface_size,
                "stretched criterion": gap_ratio_naive,
                "tilted criterion": gap_ratio_naive,
                "kind": "naive ideal",
            },
        )

        if rank >= surface_size:
            epoch = rank.bit_length() - surface_size.bit_length() + 1
            gap_ratio_upper_bound = min(
                2 * (epoch + surface_size.bit_length() - 1) / surface_size,
                4 * epoch / surface_size,
            )
        else:
            gap_ratio_upper_bound = 0

        if enforce_stretched_bound:
            assert (
                gap_ratio_upper_bound >= gap_stretched_ratios.max()
                or np.isclose(gap_ratio_upper_bound, gap_stretched_ratios.max())
            )
        if enforce_tilted_bound:
            assert (
                gap_ratio_upper_bound >= gap_tilted_ratios.max()
                or np.isclose(gap_ratio_upper_bound, gap_tilted_ratios.max())
            )

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
