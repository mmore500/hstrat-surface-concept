import itertools as it
import typing

from matplotlib import figure as mpl_figure
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

from .site_reservation_at_rank_heatmap import site_reservation_at_rank_heatmap
from .site_reservation_by_rank_heatmap import site_reservation_by_rank_heatmap


def site_reservation_by_rank_spliced_at_heatmap(
    surface_history_df: pd.DataFrame,
    splice_from_ranks: typing.List[int],
    splice_to_ranks: typing.List[int],
    reservation_mode: str = "tilted",
) -> mpl_figure.Figure:

    splice_from_ranks = sorted(splice_from_ranks)
    splice_to_ranks = sorted(splice_to_ranks)

    if len(splice_from_ranks) != len(splice_to_ranks):
        raise ValueError(
            "splice_from_ranks and splice_to_ranks must have the same length",
        )
    nsplice = len(splice_from_ranks)

    panel_lims = [
        *it.pairwise(
            sorted({0, *splice_to_ranks, 1 + max(surface_history_df["rank"])})
        ),
    ]
    npanel = len(panel_lims)
    figsize = (
        surface_history_df["site"].nunique() / 2,
        surface_history_df["rank"].nunique() / 15 + 1 + nsplice / 4,
    )

    offset = int(splice_from_ranks and splice_from_ranks[0] != 0)
    height_ratios = [
        *(x for lim in panel_lims[::-1] for x in (5, np.ptp(lim))),
        5,
    ][offset : npanel + nsplice + offset]
    fig, axs = plt.subplots(
        nrows=nsplice + npanel,
        figsize=figsize,
        ncols=1,
        height_ratios=height_ratios,
    )
    axs = axs[::-1]

    panel_axs = axs[offset::2]
    assert len(panel_axs) == npanel
    splice_axs = axs[not offset :: 2]

    for ax, panel_lim in tqdm(zip(panel_axs, panel_lims)):
        site_reservation_by_rank_heatmap(
            surface_history_df,
            ax=ax,
            cbar=False,
            reservation_mode=reservation_mode,
        )
        ax.set_ylim(*panel_lim)

    for ax, splice_from_rank in tqdm(zip(splice_axs, splice_from_ranks)):
        ax = site_reservation_at_rank_heatmap(
            surface_history_df,
            splice_from_rank,
            ax=ax,
            reservation_mode=reservation_mode,
            zigzag=False,
        )

    for ax in axs[1:]:
        ax.xaxis.set_visible(False)

    axs[0].set_xticks(
        np.array(sorted(surface_history_df["site"].unique())) + 0.5
    )
    axs[0].set_xticklabels(sorted(surface_history_df["site"].unique()))
    axs[0].set_xlabel("Buffer Position")

    return fig
