from collections import namedtuple
import typing

from matplotlib import animation as mpl_animation
from matplotlib import artist as mpl_artist
from matplotlib import patches as mpl_patches
from matplotlib import pyplot as plt
from matplotlib import ticker as mpl_ticker
import numpy as np
import pandas as pd

from ..hanoi import get_hanoi_value_at_index
from .site_ingest_depth_by_rank_heatmap import site_ingest_depth_by_rank_heatmap


def _draw_buffer_grid(
    ax: plt.Axes,
    num_sites: int,
) -> None:
    ax.set_xlim(-0.5, num_sites - 0.5)
    ax.set_ylim(0, 1)
    ax.set_xticks(np.arange(0, num_sites, 1))
    ax.set_xticklabels([*map(str, range(num_sites))])
    ax.set_yticks([])

    ax.minorticks_on()
    ax.grid(which="minor", alpha=0.5, color="gray")
    ax.tick_params(which="minor", left=False)
    ax.xaxis.set_minor_locator(mpl_ticker.AutoMinorLocator(2))


def _make_do_init(
    artists: typing.Sequence[mpl_artist.Artist],
    surface_history_df: pd.DataFrame,
    record_ax: plt.Axes,
    buffer_ax: plt.Axes,
    fig: plt.Figure,
) -> typing.Callable:

    def _do_init() -> typing.Sequence[mpl_artist.Artist]:
        site_ingest_depth_by_rank_heatmap(
            surface_history_df,
            ax=record_ax,
            cbar=False,
        )
        record_ax.set_ylim(1, 0)
        record_ax.set_xticks([])
        record_ax.set_xticklabels([])
        record_ax.set_xlabel("")
        record_ax.set_yticks([])
        record_ax.set_yticklabels([])
        _draw_buffer_grid(
            buffer_ax,
            surface_history_df["site"].max() + 1,
        )
        fig.tight_layout()

        selected_site, = artists
        buffer_ax.add_patch(selected_site)
        return selected_site,

    return _do_init


def _make_do_update(
    artists: typing.Sequence[mpl_artist.Artist],
    surface_history_df: pd.DataFrame,
    record_ax: plt.Axes,
) -> typing.Callable:

    def _do_update(rank: int) -> typing.Sequence[mpl_artist.Artist]:
        mask = (
            (surface_history_df["rank"] == rank)
            & (surface_history_df["ago"] == 0)
        )
        selected_index = (
            surface_history_df.loc[mask, "site"].squeeze() if mask.any() else -1
        )
        selected_site, = artists
        selected_site.set_xy((selected_index - 0.5, 0))

        record_ax.set_ylim(rank + 1, 0)
        return selected_site,

    return _do_update


# adapted from https://matplotlib.org/devdocs/gallery/animation/animate_decay.html#sphx-glr-gallery-animation-animate-decay-py
def typewriter_animate(
    surface_history_df: pd.DataFrame,
) -> mpl_animation.FuncAnimation:
    surface_history_df["ago"] = (
        surface_history_df["rank"] - surface_history_df["ingest rank"]
    )
    fig, (record_ax, buffer_ax) = plt.subplots(
       2,
       1,
       figsize=(10, 8),
       height_ratios=(7, 1),
    )
    selected_site = mpl_patches.Rectangle(
        (-1.5, 0),
        1,
        1,
        color="black",
        fill=True,
    )
    n_step = surface_history_df["rank"].max() + 1
    return mpl_animation.FuncAnimation(
        fig=fig,
        func=_make_do_update(
            (selected_site,),
            surface_history_df,
            record_ax,
        ),
        frames=range(n_step),
        init_func=_make_do_init(
            (selected_site,),
            surface_history_df,
            record_ax,
            buffer_ax,
            fig,
        ),
        # blit=True,
        repeat_delay=5000,
    )
