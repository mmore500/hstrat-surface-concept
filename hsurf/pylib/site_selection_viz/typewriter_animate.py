import typing

from matplotlib import animation as mpl_animation
from matplotlib import artist as mpl_artist
from matplotlib import gridspec as mpl_gridspec
from matplotlib import patches as mpl_patches
from matplotlib import pyplot as plt
from matplotlib import ticker as mpl_ticker
import numpy as np
import pandas as pd
import seaborn as sns

from .site_ingest_depth_by_rank_heatmap import (
    site_ingest_depth_by_rank_heatmap,
)


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


def _draw_record(
    ax: plt.Axes,
    mask: np.array,
) -> None:
    record = np.zeros_like(mask, dtype=int)
    record[mask] = np.flatnonzero(mask) + 1
    assert record.shape == mask.shape
    ax.clear()
    sns.heatmap(
        record[:, np.newaxis],
        mask=~mask[:, np.newaxis],
        ax=ax,
        cbar=False,
        cmap="binary",
        linewidths=1,
        linecolor="white",
        vmin=0,
        vmax=1,
    )
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_yticklabels([])


def _make_do_init(
    artists: typing.Sequence[mpl_artist.Artist],
    surface_history_df: pd.DataFrame,
    history_ax: plt.Axes,
    buffer_ax: plt.Axes,
    fig: plt.Figure,
) -> typing.Callable:

    smask0 = (surface_history_df["rank"] == 0) & (
        surface_history_df["ago"] == 0
    )
    selected_index0 = (
        surface_history_df.loc[smask0, "site"].squeeze()
        if smask0.any()
        else -1
    )

    def do_init() -> typing.Sequence[mpl_artist.Artist]:
        site_ingest_depth_by_rank_heatmap(
            surface_history_df,
            ax=history_ax,
            cbar=False,
        )
        history_ax.set_ylim(1, 0)
        history_ax.set_xticks([])
        history_ax.set_xticklabels([])
        history_ax.set_xlabel("")
        history_ax.set_yticks([])
        history_ax.set_yticklabels([])
        history_ax.set_ylabel("")
        buffer_ax.set_yticks([])
        n_site = surface_history_df["site"].max() + 1
        _draw_buffer_grid(
            buffer_ax,
            n_site,
        )
        fig.tight_layout()

        history_ax.add_patch(
            mpl_patches.Rectangle(
                (selected_index0, -1),
                1,
                1,
                color=plt.get_cmap("viridis")(0),
                fill=True,
            ),
        )

        selected_patch, *extra_patches = artists
        buffer_ax.add_patch(selected_patch)
        overwrite_patches = extra_patches[:n_site]
        for patch in overwrite_patches:
            history_ax.add_patch(patch)
        age_patches = extra_patches[n_site:]
        for patch in age_patches:
            buffer_ax.add_patch(patch)

        for site in range(n_site):
            if site == selected_index0:
                continue
            mask = (
                (surface_history_df["ago"] == 0)
                & (surface_history_df["site"] == site)
                & (
                    (surface_history_df["ingest rank"] > 0)
                    | (surface_history_df["site"] == selected_index0)
                )
            )
            height = (
                surface_history_df.loc[mask, "ingest rank"].min() - 1
                if mask.any()
                else 0
            )
            history_ax.add_patch(
                mpl_patches.Rectangle(
                    (site, 0),
                    1,
                    height,
                    color="white",
                    zorder=100,
                ),
            )

        return selected_patch, *extra_patches

    return do_init


def _make_do_update(
    artists: typing.Sequence[mpl_artist.Artist],
    surface_history_df: pd.DataFrame,
    history_ax: plt.Axes,
    record_ax: plt.Axes,
) -> typing.Callable:

    smask0 = (surface_history_df["rank"] == 0) & (
        surface_history_df["ago"] == 0
    )
    selected_index0 = (
        surface_history_df.loc[smask0, "site"].squeeze()
        if smask0.any()
        else -1
    )

    def do_update(rank: int) -> typing.Sequence[mpl_artist.Artist]:
        smask = (surface_history_df["rank"] == rank) & (
            surface_history_df["ago"] == 0
        )
        selected_index = (
            surface_history_df.loc[smask, "site"].squeeze()
            if smask.any()
            else -1
        )
        n_site = surface_history_df["site"].max() + 1
        selected_patch, *extra_patches = artists
        selected_patch.set_xy((selected_index - 0.5, 0))
        overwrite_patches = extra_patches[:n_site]
        for site, patch in enumerate(overwrite_patches):
            mask = (
                (surface_history_df["rank"] == rank)
                & (surface_history_df["site"] == site)
                & (
                    (surface_history_df["ingest rank"] > 0)
                    | (surface_history_df["site"] == selected_index0)
                )
            )
            height = (
                surface_history_df.loc[mask, "ingest rank"].squeeze()
                if mask.any()
                else 0
            )
            patch.set_height(height)
        age_patches = extra_patches[n_site:]
        for site, patch in enumerate(age_patches):
            mask = (
                (surface_history_df["rank"] == rank)
                & (surface_history_df["site"] == site)
            )
            ago = surface_history_df.loc[mask, "ago"].squeeze()
            max_rank = surface_history_df["rank"].max()
            normed_ago = np.log(ago + 1) / np.log(max_rank or 1)
            cm = plt.get_cmap("viridis")
            cm.set_bad("white")
            patch.set(color=cm(normed_ago))

        rmask = np.zeros(rank + 1, dtype=bool)
        retained_ranks = (
            surface_history_df.loc[
                (surface_history_df["rank"] == rank),
                "ingest rank",
            ]
            .dropna()
            .astype(int)
            .to_numpy()
        )
        rmask[retained_ranks] = True
        _draw_record(
            record_ax,
            rmask,
        )

        record_ax.set_ylim(rank + 1, 0)
        history_ax.set_ylim(rank, -1)

        plt.gcf().canvas.draw()

        return selected_patch, *overwrite_patches

    return do_update


# adapted from https://matplotlib.org/devdocs/gallery/animation/animate_decay.html#sphx-glr-gallery-animation-animate-decay-py
def typewriter_animate(
    surface_history_df: pd.DataFrame,
) -> mpl_animation.FuncAnimation:
    surface_history_df["ago"] = (
        surface_history_df["rank"] - surface_history_df["ingest rank"]
    )
    fig = plt.figure(figsize=(10, 8))
    gs = mpl_gridspec.GridSpec(
        2,
        2,
        height_ratios=(15, 1),
        width_ratios=(15, 1),
    )
    history_ax = fig.add_subplot(gs[0, 0])
    record_ax = fig.add_subplot(gs[0, 1])
    buffer_ax = fig.add_subplot(gs[1, 0])

    selected_patch = mpl_patches.Rectangle(
        (-1.5, 0),
        1,
        1,
        color="black",
        fill=True,
    )
    overwrite_patches = [
        mpl_patches.Rectangle(
            (i, -1),
            1,
            0,
            alpha=0.8,
            color="white",
            fill=True,
        )
        for i in range(surface_history_df["site"].max() + 1)
    ]
    ago_patches = [
        mpl_patches.Rectangle(
            (i - 0.5, 0),
            1,
            1,
            alpha=0.4,
            color="white",
            fill=True,
            zorder=-100,
        )
        for i in range(surface_history_df["site"].max() + 1)
    ]
    n_step = surface_history_df["rank"].max() + 1
    return mpl_animation.FuncAnimation(
        fig=fig,
        func=_make_do_update(
            (selected_patch, *overwrite_patches, *ago_patches),
            surface_history_df,
            history_ax,
            record_ax,
        ),
        frames=range(n_step),
        init_func=_make_do_init(
            (selected_patch, *overwrite_patches, *ago_patches),
            surface_history_df,
            history_ax,
            buffer_ax,
            fig,
        ),
        repeat_delay=5000,
    )
