import itertools as it
import os
import random
import time
import typing

from hstrat import hstrat
import pandas as pd
from tqdm import tqdm
import typing

from hsurf import hsurf

random.seed(1)


surface_size = 64
num_ops = 1000
num_replicates = 20


def iter_surface_update(
    pick_deposition_site: typing.Callable,
) -> typing.Iterable:
    surface = [None] * surface_size
    for rank in it.count():
        site = pick_deposition_site(rank, surface_size)
        surface[site] = hstrat.HereditaryStratum()
        yield


def benchmark_one(callable: typing.Callable) -> int:
    start = time.perf_counter_ns()
    for __ in range(num_ops):
        callable()
    return time.perf_counter_ns() - start


def make_hsurf_records() -> typing.List[typing.Dict]:
    return [
        {
            "Nanoseconds": benchmark_one(
                iter_surface_update(pick_deposition_site).__next__,
            ),
            "Implementation": "surface",
            "Language": "Python",
            "Num Operations": num_ops,
            "Policy": policy,
            "Replicate": replicate,
            "Surface Size": surface_size,
        }
        for (policy, pick_deposition_site), replicate in tqdm(
            it.product(
                [
                    ("steady", hsurf.steady_algo.pick_deposition_site),
                    ("tilted", hsurf.tilted_algo.pick_deposition_site),
                    (
                        "tilted-sticky",
                        hsurf.tilted_sticky_algo.pick_deposition_site,
                    ),
                    ("trivial", lambda rank, surface_size: 0),
                ],
                range(num_replicates),
            ),
        )
    ]


def make_hstrat_records() -> typing.List[typing.Dict]:
    parameterizer = hstrat.PropertyAtMostParameterizer(
        target_value=surface_size,
        policy_evaluator=hstrat.NumStrataRetainedUpperBoundEvaluator(
            at_num_strata_deposited=int(1e6),
        ),
        param_lower_bound=1,
        param_upper_bound=1024,
    )

    return [
        {
            "Nanoseconds": benchmark_one(
                hstrat.HereditaryStratigraphicColumn(
                    algo(parameterizer=parameterizer),
                    always_store_rank_in_stratum=False,
                ).DepositStratum,
            ),
            "Implementation": "column",
            "Language": "Python",
            "Num Operations": num_ops,
            "Policy": policy,
            "Replicate": replicate,
            "Surface Size": surface_size,
        }
        for (policy, algo), replicate in tqdm(
            it.product(
                [
                    (
                        "steady",
                        hstrat.depth_proportional_resolution_tapered_algo.Policy,
                    ),
                    (
                        "geom-seq-nth-root",
                        hstrat.geom_seq_nth_root_algo.Policy,
                    ),
                    (
                        "recency-proportional-resolution",
                        hstrat.recency_proportional_resolution_algo.Policy,
                    ),
                    (
                        "tilted",
                        hstrat.recency_proportional_resolution_curbed_algo.Policy,
                    ),
                    (
                        "trivial",
                        lambda parameterizer: hstrat.nominal_resolution_algo.Policy(),
                    ),
                ],
                range(num_replicates),
            ),
        )
    ]


if __name__ == "__main__":
    df = pd.DataFrame.from_records(
        [*make_hsurf_records(), *make_hstrat_records()],
    )
    os.makedirs("outdata", exist_ok=True)
    df.to_csv("outdata/a=benchmark-python-hsurf+ext=.csv", index=False)
