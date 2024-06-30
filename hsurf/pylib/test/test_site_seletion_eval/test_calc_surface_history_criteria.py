import typing

import pandas as pd
import pytest

from hsurf.site_selection_strategy import site_selection_algorithms
from pylib import site_selection_eval


@pytest.mark.parametrize(
    "surface_size, generation_cap",
    [
        (8, 2**16),
        (16, 2**16),
        (32, 2**16),
        (64, 2**14),
        (128, 2**12),
        (256, 2**12),
        pytest.param(1024, 2**12, marks=pytest.mark.heavy),
    ],
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
    generation_cap: int,
    site_selection_algo: typing.Callable,
):
    surface_history_df = site_selection_eval.make_surface_history_df(
        site_selection_algo.pick_ingest_site,
        surface_size=surface_size,
        num_generations=min(
            site_selection_algo.get_ingest_capacity(surface_size),
            generation_cap,
        ),
    )
    criteria_df = site_selection_eval.calc_surface_history_criteria(
        surface_history_df,
    )
    assert isinstance(criteria_df, pd.DataFrame)
