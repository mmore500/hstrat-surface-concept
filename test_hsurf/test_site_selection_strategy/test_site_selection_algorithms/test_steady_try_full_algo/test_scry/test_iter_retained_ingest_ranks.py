import numpy as np
import pytest

from hsurf.hsurf import steady_try_full_algo as algo


@pytest.mark.parametrize("surface_size", [2**x for x in range(1, 12)])
@pytest.mark.parametrize(
    "num_ingests",
    [
        *range(128),
        *map(int, np.linspace(0, 2**62, 100, dtype=int)),
        *map(int, np.geomspace(1, 2**62, 100, dtype=int)),
        *map(int, np.random.RandomState(seed=1).randint(0, 2**62, 100)),
    ],
)
def test_iter_retained_ingest_ranks(
    surface_size: int, num_ingests: int
) -> int:
    expected = (
        set(algo.iter_resident_ingest_ranks(surface_size, num_ingests))
        if num_ingests
        else set()
    )
    actual = [*algo.iter_retained_ingest_ranks(surface_size, num_ingests)]
    len(actual) == len(expected)
    assert expected == set(actual)
