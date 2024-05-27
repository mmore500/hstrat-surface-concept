import itertools as it
import typing

from matplotlib import axes as mpl_axes
import numpy as np
import pandas as pd
import seaborn as sns

from ._extract_reservation_indices_at_rank import (
    extract_reservation_indices_at_rank,
)


def site_reservation_at_rank_heatmap(
    surface_history_df: pd.DataFrame,
    rank: int,
    ax: typing.Optional[mpl_axes.Axes] = None,
    zigzag: bool = False,
) -> mpl_axes.Axes:

    slice_df = (
        surface_history_df[surface_history_df["rank"] == rank]
        .sort_values("site", ascending=True)
        .reset_index(drop=True)
    )
    nsite = len(slice_df)
    ax = sns.heatmap(
        data=slice_df.pivot(index="rank", columns="site", values="hanoi value"),
        ax=ax,
        cbar=False,
        cmap=sns.color_palette("tab10", 10) + sns.color_palette("deep", 10),
        vmax=20 + 0.5,  # align cbar labels
        vmin=0 - 0.5,  # align cbar labels
    )

    ax.axhline(1, color="burlywood", linewidth=12)  # alt: "burlywood"

    # this part is a mess, could be rewritten ...
    reservation_indices = extract_reservation_indices_at_rank(slice_df, rank)
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

    for hv, site in zip(slice_df["hanoi value"], slice_df["site"]):
        ax.text(
            site + 0.5,
            0.4,
            f"{int(hv)}",
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
