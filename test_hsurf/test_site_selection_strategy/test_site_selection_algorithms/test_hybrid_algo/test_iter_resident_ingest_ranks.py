import itertools as it

import numpy as np
import pytest

from hsurf.hsurf import hybrid_algo as algo


@pytest.mark.parametrize("surface_size", [2**x for x in range(2, 10)])
@pytest.mark.parametrize(
    "num_ingests",
    [
        *range(128),
        *map(int, np.linspace(0, 2**62, 100, dtype=int)),
        *map(int, np.geomspace(1, 2**62, 100, dtype=int)),
        *map(int, np.random.RandomState(seed=1).randint(0, 2**62, 100)),
    ],
)
def test_iter_resident_ingest_ranks(surface_size: int, num_ingests: int) -> int:
    if num_ingests > algo.get_ingest_capacity(surface_size):
        return

    expected = (
        algo.calc_resident_ingest_rank(site, surface_size, num_ingests)
        for site in range(surface_size)
    )
    actual = algo.iter_resident_ingest_ranks(surface_size, num_ingests)
    assert all(it.starmap(int.__eq__, zip(actual, expected, strict=True)))
