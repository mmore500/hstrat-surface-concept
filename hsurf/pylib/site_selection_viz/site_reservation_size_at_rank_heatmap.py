import itertools as it
import typing

from matplotlib import axes as mpl_axes
import numpy as np
import pandas as pd
import seaborn as sns

from ._extract_reservation_indices_at_rank import (
    extract_reservation_indices_at_rank,
)


def site_reservation_size_at_rank_heatmap(
    surface_history_df: pd.DataFrame,
    rank: int,
    ax: typing.Optional[mpl_axes.Axes] = None,
    reservation_mode: str = "tilted",
    zigzag: bool = False,
) -> mpl_axes.Axes:

    slice_df = (
        surface_history_df[surface_history_df["rank"] == rank]
        .sort_values("site", ascending=True)
        .reset_index(drop=True)
    )
    nsite = len(slice_df)
    reservation_indices = [
        *extract_reservation_indices_at_rank(
            slice_df, rank, reservation_mode=reservation_mode
        ),
    ]
    reservation_bounds = [
        *it.pairwise(
            [
                *reservation_indices,
                nsite,
            ],
        )
    ]
    reservation_sizes = [
        *map(
            np.ptp,
            reservation_bounds,
        ),
    ]

    epoch = max(
        0,
        rank.bit_length() - nsite.bit_length() + (rank.bit_count() > 1),
    )
    next_epoch = epoch + 1
    if epoch == 0:
        mask = [[False] * nsite]
    elif (next_epoch + next_epoch.bit_length()).bit_count() <= 1:
        mask = [
            [
                size != min(reservation_sizes)
                for size in reservation_sizes
                for __ in range(size)
            ]
        ]
    else:
        mask = [[True] * nsite]

    cmap = sns.color_palette("flare", nsite.bit_length(), as_cmap=True)
    cmap.set_bad("lightgray")
    ax = sns.heatmap(
        data=np.array(
            [
                [
                    int(size).bit_length() if epoch else size
                    for size in reservation_sizes
                    for __ in range(size)
                ]
            ],
        ),
        mask=np.array(mask),
        ax=ax,
        cbar=False,
        cmap=cmap,
        vmax=nsite.bit_length(),  # align cbar labels
        vmin=1,  # align cbar labels
    )

    # this part is a mess, could be rewritten
    reservation_indices = extract_reservation_indices_at_rank(
        slice_df, rank, reservation_mode=reservation_mode
    )
    for last_site, site in it.pairwise((None, *reservation_indices, nsite)):
        ax.axvline(site, color="white", linewidth=12)
        if site == 0:
            continue
        if zigzag:
            if site != nsite:
                ax.axvline(
                    site, -0.5, 1.5, color="black", linewidth=2, clip_on=False
                )
            if last_site and site - last_site == min(
                np.diff([*reservation_indices, nsite])
            ):
                xmax = ax.get_xlim()[1]
                ax.axhline(
                    -0.5,
                    (last_site) / xmax,
                    (last_site + 1) / xmax,
                    color="black",
                    linewidth=2,
                    clip_on=False,
                )
        elif site != nsite:
            ax.axvline(site, color="black", linewidth=2)
    # ... end of mess

    ax.axvline(slice_df["site"].max() + 1, color="white", linewidth=4)

    for lb, ub in reservation_bounds:
        if epoch == 0 or (
            (next_epoch + next_epoch.bit_length()).bit_count() <= 1
            and ub - lb == min(reservation_sizes)
        ):
            ax.text(
                lb + (ub - lb) / 2,
                0.5,
                ("R=" if epoch else "r=") * (ub - lb > 1) + f"{int(ub - lb)}",
                color="white",
                ha="center",
                va="center",
                fontweight="bold",
            )

    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")

    return ax
