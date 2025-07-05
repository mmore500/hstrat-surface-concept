import typing

from hstrat import hstrat
from matplotlib import axes as mpl_axes
import numpy as np
import pandas as pd

from ._SurfaceHistoryToStratumRetentionPolicyShim import (
    SurfaceHistoryToStratumRetentionPolicyShim,
)


def stratum_persistence_dripplot(
    surface_history_df: pd.DataFrame,
    progress_wrap: typing.Callable = lambda x: x,
) -> mpl_axes.Axes:
    policy_shim = SurfaceHistoryToStratumRetentionPolicyShim(surface_history_df)
    ax = hstrat.stratum_retention_dripplot(
        policy_shim,
        surface_history_df["rank"].max(),
        progress_wrap=progress_wrap,
    )
    ax.set_ylabel("Time")
    ax.set_xlabel("Ingestion Time Point")
    ax.tick_params(axis="x", rotation=0)
    ax.autoscale(enable=True, axis="x", tight=True)
    xticks = np.linspace(*ax.get_xlim(), num=9, dtype=int)
    ax.set_xticks(xticks - xticks.min(), xticks - xticks.min())
    for spine in ax.spines.values():
        spine.set_visible(False)
    return ax
