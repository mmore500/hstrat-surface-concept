import typing

from matplotlib import figure as mpl_figure
from matplotlib import pyplot as plt
import pandas as pd

from .site_reservation_at_rank_heatmap import site_reservation_at_rank_heatmap


def site_reservation_at_ranks_heatmap(
    surface_history_df: pd.DataFrame,
    ranks: typing.List[int],
) -> mpl_figure.Figure:

    figsize = (surface_history_df["site"].nunique() / 2, len(ranks) / 2)

    fig, axs = plt.subplots(nrows=len(ranks), figsize=figsize, ncols=1)
    for rank, ax in zip(ranks, axs[::-1]):
        site_reservation_at_rank_heatmap(
            surface_history_df, rank, ax=ax, zigzag=True
        )

    fig.subplots_adjust(hspace=1.0)

    return fig
