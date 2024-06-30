import types
import typing

import numpy as np
import pandas as pd


def calc_surface_history_criteria(
    surface_history_df: pd.DataFrame,
    site_selection_algo: types.ModuleType,
    site_selection_bounds: types.ModuleType,  # workaround for levelization
    site_selection_criteria: types.ModuleType,  # workaround for levelization
    enforce_tilted_bound: bool = False,
    enforce_steady_bound: bool = False,
    enforce_stretched_bound: bool = False,
    progress_wrap: typing.Callable = lambda x: x,
) -> pd.DataFrame:

    surface_size = int(surface_history_df["site"].max() + 1)

    records = []
    for rank, group_df in progress_wrap(
        surface_history_df[surface_history_df["ingest rank"] != -1].groupby(
            "rank"
        ),
    ):
        retained_ranks = sorted(group_df["ingest rank"])
        gap_bounds = site_selection_criteria._impl.calc_gap_bounds(
            retained_ranks, rank + 1
        )
        gap_sizes = (
            site_selection_criteria._impl.calc_gap_sizes_from_gap_bounds(
                gap_bounds
            )
        )

        csr = site_selection_criteria._calc_stretched_ratios
        gap_stretched_ratios = csr._calc_stretched_ratios_from_gaps(
            gap_bounds, gap_sizes
        )

        ctr = site_selection_criteria._calc_tilted_ratios
        gap_tilted_ratios = ctr._calc_tilted_ratios_from_gaps(
            gap_bounds, gap_sizes, rank + 1
        )

        records.append(
            {
                "rank": rank,
                "steady criterion": gap_sizes.max(),
                "stretched criterion": gap_stretched_ratios.max(),
                "tilted criterion": gap_tilted_ratios.max(),
                "kind": "maximum",
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

        gap_ratio_ideal = (
            site_selection_bounds._impl.calc_gap_ratio_lower_bound(
                surface_size, rank + 1
            )
            if rank < 2**surface_size
            else np.nan
        )
        assert (
            gap_ratio_ideal <= gap_stretched_ratios.max()
            or np.isclose(gap_ratio_ideal, gap_stretched_ratios.max())
            or rank >= 2**surface_size
        )
        assert (
            gap_ratio_ideal <= gap_tilted_ratios.max()
            or np.isclose(gap_ratio_ideal, gap_tilted_ratios.max())
            or rank >= 2**surface_size
        )

        gap_size_ideal = site_selection_bounds.calc_gap_size_lower_bound(
            surface_size, rank + 1
        )
        assert gap_size_ideal <= gap_sizes.max() or np.isclose(
            gap_size_ideal, gap_sizes.max()
        )

        records.append(
            {
                "rank": rank,
                "steady criterion": gap_size_ideal,
                "stretched criterion": gap_ratio_ideal,
                "tilted criterion": gap_ratio_ideal,
                "kind": "lower bound",
            },
        )

        gap_ratio_naive = max(rank ** (1 / surface_size) - 1, 0)
        records.append(
            {
                "rank": rank,
                "steady criterion": rank / surface_size,
                "stretched criterion": gap_ratio_naive,
                "tilted criterion": gap_ratio_naive,
                "kind": "naive lower bound",
            },
        )

        stretched_gap_ratio_upper_bound = (
            site_selection_algo.calc_stretched_criterion_upper_bound(
                surface_size, rank + 1
            )
        )
        if enforce_stretched_bound:
            assert (
                stretched_gap_ratio_upper_bound >= gap_stretched_ratios.max()
                or np.isclose(
                    stretched_gap_ratio_upper_bound, gap_stretched_ratios.max()
                )
            )

        tilted_gap_ratio_upper_bound = (
            site_selection_algo.calc_tilted_criterion_upper_bound(
                surface_size, rank + 1
            )
        )
        if enforce_tilted_bound:
            assert (
                tilted_gap_ratio_upper_bound >= gap_tilted_ratios.max()
                or np.isclose(
                    tilted_gap_ratio_upper_bound, gap_tilted_ratios.max()
                )
            )

        steady_gap_size_upper_bound = (
            site_selection_algo.calc_steady_criterion_upper_bound(
                surface_size, rank + 1
            )
        )
        if enforce_steady_bound:
            assert steady_gap_size_upper_bound >= gap_sizes.max() or np.isclose(
                steady_gap_size_upper_bound, gap_sizes.max()
            )

        records.append(
            {
                "rank": rank,
                "steady criterion": steady_gap_size_upper_bound,
                "stretched criterion": stretched_gap_ratio_upper_bound,
                "tilted criterion": tilted_gap_ratio_upper_bound,
                "kind": "upper bound",
            },
        )

    return pd.DataFrame.from_records(records)
