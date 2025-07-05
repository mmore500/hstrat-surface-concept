import typing

from matplotlib import figure as mpl_figure
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from .site_reservation_at_rank_heatmap import site_reservation_at_rank_heatmap


def site_reservation_at_ranks_heatmap(
    surface_history_df: pd.DataFrame,
    ranks: typing.List[int],
    color_epoch_t: typing.Optional[str] = None,
    color_metaepoch_tau: typing.Optional[str] = None,
    color_site_k: typing.Optional[str] = None,
    reservation_mode: str = "tilted",
    swap_yaxes: bool = False,
    zigzag: bool = True,
    plotter_: typing.Callable = site_reservation_at_rank_heatmap,
) -> mpl_figure.Figure:

    if color_epoch_t is None:
        color_epoch_t = "#EF58A0"
    if color_metaepoch_tau is None:
        color_metaepoch_tau = "#ff7f00"
    if color_site_k is None:
        color_site_k = "#be0040"

    figsize = (surface_history_df["site"].nunique() / 2, len(ranks) / 2)

    fig, axs = plt.subplots(
        nrows=len(ranks) + 1,
        ncols=3,
        figsize=figsize,
        gridspec_kw={
            "width_ratios": [
                1 / surface_history_df["site"].nunique(),
                1,
                1 / surface_history_df["site"].nunique(),
            ],
            "wspace": 0,
        },
    )

    for rank, ax in zip(ranks, axs[:-1, 1][::-1]):
        plotter_(
            surface_history_df,
            rank,
            ax=ax,
            reservation_mode=reservation_mode,
            zigzag=zigzag,
        )

    fig.subplots_adjust(hspace=1.0)

    axs[-2, 1].set_xticks(
        np.array(sorted(surface_history_df["site"].unique())) + 0.5
    )
    axs[-2, 1].set_xticklabels(sorted(surface_history_df["site"].unique()))

    for epoch, ax in enumerate(reversed(axs[:-1, 1])):
        ax.set_yticks([0.5])
        ax.set_yticklabels([f"{epoch}"])
        for tick in ax.get_yticklabels():
            tick.set_rotation(0)

        if (epoch + epoch.bit_length()).bit_count() <= 1:
            ax2 = ax.twinx()
            ax2.set_frame_on(False)
            ax2.set_ylim(ax.get_ylim())
            ax2.set_yticks([0.5])
            meta_epoch = max(
                (epoch + epoch.bit_length()).bit_length() - 1,
                0,
            )
            ax2.set_yticklabels(
                [
                    f"""\n{meta_epoch}\n—""",
                ]
            )
            for tick in ax2.get_yticklabels():
                tick.set_rotation(0)
            if "steady" not in reservation_mode and meta_epoch:
                ax2.axhline(
                    1.5,
                    0,
                    1,
                    color="black",
                    linewidth=1,
                    linestyle="--",
                    clip_on=False,
                )

        if swap_yaxes:
            ax.yaxis.tick_right()
            ax.yaxis.set_label_position("right")
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.set_yticklabels(
                ax.get_yticklabels(),
                rotation=0,
            )

            ax2.yaxis.tick_left()
            ax2.yaxis.set_label_position("left")
            ax2.spines["left"].set_visible(False)
            ax2.spines["right"].set_visible(False)
            ax2.set_yticklabels(
                ax2.get_yticklabels(),
                rotation=0,
            )

    # Draw labels onto edge axes...
    # Left edge, epoch
    for ax in axs[:, 0]:
        ax.axis("off")
    axs[(len(ranks) - 1) // 2, 0].text(
        0.0,
        0.5,
        ["Epoch", "Meta-epoch"][swap_yaxes],
        rotation=90,
        ha="center",
        va="center",
        fontsize=10,
    )
    axs[(len(ranks) - 1) // 2, 0].text(
        0.0,
        0.5,
        ["           t", "                    τ"][swap_yaxes],
        color=[color_epoch_t, color_metaepoch_tau][swap_yaxes],
        rotation=90,
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
    )

    # Right edge, meta-epoch
    for ax in axs[:, 2]:
        ax.axis("off")
    axs[(len(ranks) - 1) // 2, 2].text(
        1.0,
        0.5,
        ["Meta-epoch", "Epoch"][swap_yaxes],
        rotation=-90,
        ha="center",
        va="center",
        fontsize=10,
    )
    axs[(len(ranks) - 1) // 2, 2].text(
        1.0,
        0.5,
        ["                    τ", "           t"][swap_yaxes],
        color=[color_metaepoch_tau, color_epoch_t][swap_yaxes],
        rotation=-90,
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        style="italic",
    )

    # Bottom, site
    axs[-1, 1].axis("off")
    axs[-1, 1].text(
        0.5,
        0,
        "Buffer Site",
        fontsize=10,
        ha="center",
        va="center",
    )
    axs[-1, 1].text(
        0.5,
        0,
        "                    k",
        color=color_site_k,
        fontsize=10,
        fontweight="bold",
        style="italic",
        ha="center",
        va="center",
    )

    return fig
