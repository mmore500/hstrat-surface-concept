import string

from matplotlib import axes as mpl_axes
from matplotlib.ticker import StrMethodFormatter as mpl_StrMethodFormatter
import more_itertools as mit
import pandas as pd
import seaborn as sns

from ._LegendPatchHandler import LegendPatchHandler


def criterion_satisfaction_lineplot(
    data: pd.DataFrame,
    x: str,
    y: str,
    hue: str,
    surface_size: int,
    xscale: str = "log",
    yscale: str = "linear",
) -> mpl_axes.Axes:
    """Plot criterion value as ingests elapse, with lower and upper bounds.

    See Also
    --------
    calc_surface_history_criteria : source for `data` DataFrame.
    """
    data = data.copy()
    data["kind"] = (
        data["kind"]
        .str.replace("mean", "actual: mean")
        .replace("maximum", "actual: extremum")
        .replace("upper bound", "bound: extremum")
        .replace("lower bound", "ideal: extremum")
    )
    lower_bound = "ideal: extrema"
    upper_bound = "bound: extrema"
    hue_order = sorted(
        data[hue].unique(),
        key=lambda x: (-(x == lower_bound), -(x == upper_bound), x),
        reverse=True,
    )
    palette = [
        sns.color_palette("husl", len(hue_order) - 1)[-1],
        "dimgray",
        *sns.color_palette("husl", len(hue_order) - 1)[:-1],
    ]

    # LINEPLOT ################################################################
    ax = sns.lineplot(
        data=data[~data[hue].isin([lower_bound, upper_bound])],
        x=x,
        y=y,
        hue=hue,
        hue_order=hue_order,
        style=hue,
        style_order=[hue_order[1], hue_order[0], *hue_order[2:]],
        errorbar=lambda xs: (0.1, 10),
        palette=palette,
    )
    frozen_ylim = ax.get_ylim()

    # FILLED BOUNDS ###########################################################
    filtered = data[data[hue] == upper_bound]
    # sns err needs at least two observations...
    duplicated = pd.concat([filtered] * 2, ignore_index=True)
    sns.lineplot(
        data=duplicated,
        x=x,
        y=y,
        hue=hue,
        hue_order=hue_order,
        ax=ax,
        errorbar=lambda xs: (mit.one(set(xs)), ax.get_ylim()[1]),
        linewidth=0.0,
        legend=False,
        palette=palette,
        zorder=-10,
    )

    filtered = data[data[hue] == lower_bound]
    # sns err needs at least two observations...
    duplicated = pd.concat([filtered] * 2, ignore_index=True)
    sns.lineplot(
        data=duplicated,
        x=x,
        y=y,
        hue=hue,
        hue_order=hue_order,
        ax=ax,
        errorbar=lambda xs: (min(-1, ax.get_ylim()[0]), mit.one(set(xs))),
        legend=False,
        linewidth=0.0,
        palette=palette,
        zorder=-10,
    )

    # AXES TWEAKS #############################################################
    ax.set_xlabel("Time")
    ax.set_ylabel("Criterion\nValue")
    ax.spines[["top", "right"]].set_visible(False)

    ax.set_xscale(xscale)
    ax.set_yscale(yscale)
    if yscale == "symlog":  # force non-scientific notation
        ax.yaxis.set_major_formatter(mpl_StrMethodFormatter("{x:.0f}"))

    for x in range(surface_size.bit_length() - 1, surface_size):
        ax.axvline(2**x, color="black", linestyle="--", linewidth=0.5)

    # LEGEND ##################################################################
    handles, labels = ax.get_legend_handles_labels()

    # Setting the legend with the new compound handles
    ax.legend(
        handles,
        labels,
        handler_map={
            handles[hue_order.index(upper_bound)]: LegendPatchHandler(),
            handles[hue_order.index(lower_bound)]: LegendPatchHandler(),
        },
        frameon=False,
        title=string.capwords(y),
    )

    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))

    # RESTORE YLIM ############################################################
    ax.set_ylim(-0.1, frozen_ylim[1])  # restoring low ylim is wonky, hardcode

    return ax
