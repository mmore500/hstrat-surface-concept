import typing

from matplotlib import axes as mpl_axes
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from ..Literal import Literal
from ._apply_pseudo_linear_yticks import apply_pseudo_linear_yticks
from ._apply_pseudo_log_yticks import apply_pseudo_log_yticks
from ._geomspace_filter_surface_history_df import (
    geomspace_filter_surface_history_df,
)
from ._linspace_filter_surface_history_df import (
    linspace_filter_surface_history_df,
)


def site_differentia_by_rank_heatmap(
    surface_history_df: pd.DataFrame,
    ynorm: typing.Optional[Literal["log", "linear"]] = "log",  # noqa: F821
    rank_sample_size: int = 256,
    figsize: typing.Optional[typing.Tuple[int, int]] = None,
) -> mpl_axes.Axes:
    # Reshape data
    if ynorm == "log":
        filtered_df = geomspace_filter_surface_history_df(
            surface_history_df,
            rank_sample_size,
        )
    else:
        assert ynorm in ("linear", None)
        filtered_df = linspace_filter_surface_history_df(
            surface_history_df,
            rank_sample_size,
        )
    reshaped_df = filtered_df.pivot_table(
        index="rank",
        columns="site",
        values="differentia",
    )

    # Create heatmap
    if figsize is not None:
        plt.figure(figsize=figsize)
    ax = sns.heatmap(reshaped_df, cmap="viridis", annot=False)
    ax.figure.set_dpi(500)
    ax.figure.axes[-1].get_children()[1].set_rasterized(True)

    if ynorm == "log":
        ax = apply_pseudo_log_yticks(ax)
    elif ynorm == "linear":
        ax = apply_pseudo_linear_yticks(ax)
    else:
        assert ynorm is None

    ax.set_ylim(*reversed(ax.get_ylim()))
    ax.set_ylabel("Time")
    ax.set_xlabel("Buffer Position")
    xticks = np.linspace(*ax.get_xlim(), num=9, dtype=int)
    ax.set_xticks(xticks, xticks)
    ax.tick_params(axis="x", rotation=0)

    return ax
