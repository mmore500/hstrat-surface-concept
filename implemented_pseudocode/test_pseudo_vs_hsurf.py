import itertools as it

import numpy as np
import opytional as opyt
import pytest

from .hsurf import hsurf
from .steady_site_selection import steady_site_selection
from .stretched_site_selection import stretched_site_selection
from .tilted_site_selection import tilted_site_selection


@pytest.mark.parametrize("S", [2**s for s in range(2, 21)])
def test_pseudo_vs_hsurf_steady(S: int):
    algo = hsurf.steady_try_full_algo
    T_max = min(
        opyt.or_value(algo.get_ingest_capacity(S), np.inf), 2**64 - 1
    )
    for T in it.chain(
        range(min(T_max, 10**5)),
        map(
            int,
            np.random.RandomState(1).randint(
                0, T_max, 10**4, dtype=np.uint64
            ),
        ),
    ):
        expected = algo.pick_ingest_site(T, S)
        actual = steady_site_selection(S, T)
        assert opyt.or_value(actual, S) == expected


@pytest.mark.parametrize(
    "S",
    [
        pytest.param(2**s, marks=pytest.mark.heavy if s >= 10 else [])
        for s in range(2, 21)
    ],
)
def test_pseudo_vs_hsurf_stretched(S: int):
    algo = hsurf.stretched_try_algo
    T_max = min(
        opyt.or_value(algo.get_ingest_capacity(S), np.inf), 2**64 - 1
    )
    for T in it.chain(
        range(min(T_max, 10**5)),
        map(
            int,
            np.random.RandomState(1).randint(
                0, T_max, 10**4, dtype=np.uint64
            ),
        ),
    ):
        expected = algo.pick_ingest_site(T, S)
        actual = stretched_site_selection(S, T)
        assert opyt.or_value(actual, S) == expected


@pytest.mark.parametrize(
    "S",
    [
        pytest.param(2**s, marks=pytest.mark.heavy if s >= 10 else [])
        for s in range(2, 21)
    ],
)
def test_pseudo_vs_hsurf_tilted(S: int):
    algo = hsurf.tilted_algo
    T_max = min(
        opyt.or_value(algo.get_ingest_capacity(S), np.inf), 2**64 - 1
    )
    for T in it.chain(
        range(min(T_max, 10**5)),
        map(
            int,
            np.random.RandomState(1).randint(
                0, T_max, 10**4, dtype=np.uint64
            ),
        ),
    ):
        expected = algo.pick_ingest_site(T, S)
        actual = tilted_site_selection(S, T)
        assert opyt.or_value(actual, S) == expected
