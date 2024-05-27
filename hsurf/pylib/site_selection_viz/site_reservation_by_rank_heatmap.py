import typing

import matplotlib as mpl
from matplotlib import axes as mpl_axes
import numpy as np
import pandas as pd
import seaborn as sns

from ..webfont import make_fontproperties
from ._extract_reservation_indices_at_rank import (
    extract_reservation_indices_at_rank,
)


def site_reservation_by_rank_heatmap(
    surface_history_df: pd.DataFrame,
    ax: typing.Optional[mpl_axes.Axes] = None,
    cbar: bool = True,
) -> mpl_axes.Axes:
    surface_history_df = (
        surface_history_df.replace(-1, np.nan)
        .sort_values("rank", ascending=False)
        .copy()
    )
    surface_history_df["ago"] = (
        surface_history_df["rank"] - surface_history_df["deposition rank"]
    )
    surface_history_df["new"] = (
        surface_history_df["rank"] == surface_history_df["deposition rank"]
    ).map({True: "⬬", False: ""})

    ax = sns.heatmap(
        data=surface_history_df.pivot(
            index="rank", columns="site", values="hanoi value"
        ),
        annot=surface_history_df.pivot(
            index="rank", columns="site", values="new"
        ),
        annot_kws=dict(
            fontproperties=make_fontproperties(
                "https://github.com/stipub/stixfonts/raw/f120869ef6853e187514917dc8c2b99adfded140/fonts/static_ttf/STIXTwoMath-Regular.ttf",
            ),
            fontsize=4,
            color="lightyellow",
            clip_on=True,
        ),
        ax=ax,
        cbar=cbar,
        cbar_kws=dict(label="hanoi value"),
        cmap=sns.color_palette(
            "bright", surface_history_df["hanoi value"].nunique()
        ),
        fmt="s",
        linewidths=0.5,
        linecolor="black",
        vmax=surface_history_df["hanoi value"].max() + 0.5,  # align cbar labels
        vmin=surface_history_df["hanoi value"].min() - 0.5,  # align cbar labels
    )
    sns.heatmap(
        surface_history_df.pivot(index="rank", columns="site", values="ago"),
        norm=mpl.colors.LogNorm(vmin=0.01),
        cmap="gray",
        ax=ax,
        alpha=0.8,
        cbar=False,
    )
    ax.invert_yaxis()
    for rank, group in surface_history_df.groupby("rank"):
        reservation_sites = extract_reservation_indices_at_rank(
            group.reset_index(), rank
        )
        ax.vlines(
            reservation_sites,
            rank,
            rank + 1,
            color="white",
            linewidth=2,
            zorder=10,
        )

    for site, group in surface_history_df.dropna().groupby("site"):
        dfg = group.sort_values("rank").reset_index(drop=True)
        changeover_ranks = dfg[dfg["hanoi value"].diff().astype(bool)]["rank"]
        ax.hlines(
            changeover_ranks,
            site,
            site + 1,
            color="white",
            linewidth=2,
            zorder=10,
        )

    return ax
