from matplotlib import axes as mpl_axes
import pandas as pd
import seaborn as sns


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

    ax = sns.lineplot(
        data=data,
        x=x,
        y=y,
        hue=hue,
    )
    ax.set_xlabel("time")
    ax.set_ylabel(y.replace(" ", "\n"))
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)

    for x in range(surface_size.bit_length() - 1, surface_size):
        ax.axvline(2**x, color="black", linestyle="--", linewidth=0.5)

    return ax
