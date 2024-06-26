import itertools as it
import random
import typing

from hstrat import _auxiliary_lib as hstrat_auxlib
import pandas as pd

from ..hanoi import get_hanoi_value_at_index


def _make_surface_history_df_impl(
    get_ingest_site_at_rank_impl: typing.Callable,
    surface_size: int,
    num_generations: int,
    progress_wrap: typing.Callable = lambda x: x,
) -> pd.DataFrame:

    surface_hanoi_values = [-1] * surface_size
    surface_ingest_ranks = [-1] * surface_size
    surface_differentia = [random.choice([0, 1]) for __ in range(surface_size)]

    surface_history_records = []
    for generation in progress_wrap(range(num_generations)):
        target_site = get_ingest_site_at_rank_impl(
            generation, surface_size
        )
        hanoi_value = get_hanoi_value_at_index(generation)

        if target_site != surface_size:
            surface_differentia[target_site] = random.choice([0, 1])
            surface_hanoi_values[target_site] = hanoi_value
            surface_ingest_ranks[target_site] = generation

        for site, ingest_rank, differentia, hanoi_value in zip(
            it.count(),
            surface_ingest_ranks,
            surface_differentia,
            surface_hanoi_values,
        ):
            assert ingest_rank <= generation
            surface_history_records.append(
                {
                    "differentia": differentia,
                    "hanoi value": hanoi_value,
                    "rank": generation,
                    "site": site,
                    "ingest depth": generation - ingest_rank,
                    "ingest rank": ingest_rank,
                }
            )

    surface_history_df = pd.DataFrame.from_records(surface_history_records)
    return surface_history_df


def make_surface_history_df(
    get_ingest_site_at_rank_impl: typing.Callable,
    surface_size: int,
    num_generations: int,
    progress_wrap: typing.Callable = lambda x: x,
    random_seed: int = 1,
) -> pd.DataFrame:

    with hstrat_auxlib.RngStateContext(seed=random_seed):
        return _make_surface_history_df_impl(
            get_ingest_site_at_rank_impl,
            surface_size,
            num_generations,
            progress_wrap,
        )
