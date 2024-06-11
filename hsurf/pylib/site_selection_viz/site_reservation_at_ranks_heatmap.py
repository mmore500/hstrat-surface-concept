import typing

from matplotlib import figure as mpl_figure
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from .site_reservation_at_rank_heatmap import site_reservation_at_rank_heatmap


def site_reservation_at_ranks_heatmap(
    surface_history_df: pd.DataFrame,
    ranks: typing.List[int],
    reservation_mode: str = "tilted",
    zigzag: bool = True,
) -> mpl_figure.Figure:

    figsize = (surface_history_df["site"].nunique() / 2, len(ranks) / 2)

    fig, axs = plt.subplots(nrows=len(ranks), figsize=figsize, ncols=1)
    for rank, ax in zip(ranks, axs[::-1]):
        site_reservation_at_rank_heatmap(
            surface_history_df,
            rank,
            ax=ax,
            reservation_mode=reservation_mode,
            zigzag=zigzag,
        )

    fig.subplots_adjust(hspace=1.0)

    axs[-1].set_xticks(
        np.array(sorted(surface_history_df["site"].unique())) + 0.5
    )
    axs[-1].set_xticklabels(sorted(surface_history_df["site"].unique()))
    axs[-1].set_xlabel("Buffer Position")

    for epoch, ax in enumerate(reversed(axs)):
        ax.set_yticks([0.5])
        ax.set_yticklabels([f"Epoch {epoch}"])
        for tick in ax.get_yticklabels():
            tick.set_rotation(0)

    return fig
