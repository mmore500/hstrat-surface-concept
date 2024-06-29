import itertools as it

import numpy as np
import pytest

from hsurf.hsurf import stretched_try_algo as algo


@pytest.mark.parametrize("surface_size", [2**x for x in range(1, 10)])
@pytest.mark.parametrize(
    "num_depositions",
    [
        *range(128),
        *map(int, np.linspace(0, 2**62, 10, dtype=int)),
        *map(int, np.geomspace(1, 2**62, 10, dtype=int)),
        *map(int, np.random.RandomState(seed=1).randint(0, 2**62, 10)),
    ],
)
def test_iter_resident_deposition_ranks(
    surface_size: int, num_depositions: int
) -> int:
    if num_depositions >= 2 ** surface_size.bit_length():
        return
    expected = (
        algo.calc_resident_deposition_rank(site, surface_size, num_depositions)
        for site in range(surface_size)
    )
    actual = algo.iter_resident_deposition_ranks(surface_size, num_depositions)
    assert all(it.starmap(int.__eq__, zip(actual, expected, strict=True)))
