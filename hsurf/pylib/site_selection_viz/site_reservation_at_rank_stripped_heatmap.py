import itertools as it
import typing

from matplotlib import axes as mpl_axes
from matplotlib import patches as mpl_patches
import numpy as np
import pandas as pd
import seaborn as sns

from ._extract_reservation_indices_at_rank import (
    extract_reservation_indices_at_rank,
)


def site_reservation_at_rank_stripped_heatmap(
    surface_history_df: pd.DataFrame,
    rank: int,
    ax: typing.Optional[mpl_axes.Axes] = None,
    palette: typing.Optional[list] = None,
    reservation_mode: str = "tilted",
    zigwidth: float = 2.0,
    zigzag: bool = False,
) -> mpl_axes.Axes:

    if palette is None:
        palette = sns.color_palette("tab10", 10) + sns.color_palette(
            "pastel", 10
        )

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
        cmap=palette,
        vmax=19.9,  # align cbar labels
        vmin=0,  # align cbar labels
    )

    # this part is a mess, could be rewritten
    reservation_indices = extract_reservation_indices_at_rank(
        slice_df, rank, reservation_mode=reservation_mode
    )
    last_diff = None
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
                    linewidth=zigwidth,
                    clip_on=False,
                )
        elif (last_site != 0 and site - last_site != last_diff) or (
            site == nsite and "steady_full" not in reservation_mode
        ):
            ax.axvline(last_site, color="black", linewidth=zigwidth)
        last_diff = site - last_site
    # ... end of mess

    ax.axvline(slice_df["site"].max() + 1, color="white", linewidth=4)

    for hv, site in zip(slice_df["hanoi value"], slice_df["site"]):
        if np.isnan(hv):
            continue

        if (
            reservation_mode != "tilted"
            or rank == slice_df["site"].max()
            or (
                slice_df.loc[
                    slice_df["site"] == site - hv, "hanoi value"
                ].item()
                == 0
                and (
                    not (slice_df["site"] == site + 1).any()
                    or slice_df.loc[
                        slice_df["site"] == site + 1, "hanoi value"
                    ].item()
                    < hv
                )
            )
        ):
            ax.text(
                site + 0.5,
                0.5,
                f"{int(hv)}",
                color="white",
                ha="center",
                va="center",
                fontweight="bold",
            )
        else:
            ax.add_patch(
                mpl_patches.Rectangle(
                    (site, 0.0),
                    1,
                    1,
                    alpha=0.9,
                    color="white",
                    lw=None,
                    transform=ax.transData,
                )
            )

    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")

    return ax
