import typing

import pandas as pd
import pytest

from hsurf.site_selection_strategy import site_selection_algorithms
from pylib import site_selection_eval


@pytest.mark.parametrize(
    "surface_size",
    [8, 16, 32, 64, 128, 256, 1024],
)
@pytest.mark.parametrize(
    "site_selection_algo",
    [
        site_selection_algorithms.steady_try_algo,
        site_selection_algorithms.stretched_try_algo,
        site_selection_algorithms.tilted_algo,
    ],
)
def test_calc_surface_history_criteria_invariants(
    surface_size: int,
    site_selection_algo: typing.Callable,
):
    surface_history_df = site_selection_eval.make_surface_history_df(
        site_selection_algo.pick_deposition_site,
        surface_size=surface_size,
        num_generations=min(2**surface_size - 1, 2**16),
    )
    criteria_df = site_selection_eval.calc_surface_history_criteria(
        surface_history_df,
    )
    assert isinstance(criteria_df, pd.DataFrame)
