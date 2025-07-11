import itertools as it
import typing

from matplotlib import figure as mpl_figure
from matplotlib import patheffects as mpl_fx
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
    strip_plotter: typing.Callable = site_reservation_at_rank_heatmap,
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
        ymin, ymax = panel_lim
        yticks = [
            ymin,
            *(y for y in range(ymin + 3, ymax - 2) if y % 8 == 0),
            ymax - 1,
        ]
        ax.set_yticks(np.array(yticks) + 0.5)
        ax.set_yticklabels(yticks)

        for __, row in surface_history_df[
            (surface_history_df["rank"] == surface_history_df["ingest rank"])
            & surface_history_df["rank"]
            .astype(int)
            .isin(range(ymin, ymax))
        ].iterrows():
            offset = -3
            ax.text(
                row["site"] + 0.5,
                row["rank"] + offset,
                int(row["rank"]),
                clip_on=False,
                horizontalalignment="center",
                verticalalignment="center",
            ).set_path_effects(
                [
                    mpl_fx.Stroke(linewidth=3, foreground="1.0"),
                    mpl_fx.Normal(),
                ],
            )

    for ax, splice_from_rank in tqdm(zip(splice_axs, splice_from_ranks)):
        ax = strip_plotter(
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

    for epoch, ax in enumerate(splice_axs):
        ax.set_yticks([0.5])
        ax.set_yticklabels([f"↑ Epoch {epoch}"])
        for tick in ax.get_yticklabels():
            tick.set_rotation(0)

        line = plt.Line2D(xdata=[-2, 0], ydata=[1, 1], color="k", linewidth=1)
        line.set_clip_on(False)
        ax.add_line(line)

    return fig
