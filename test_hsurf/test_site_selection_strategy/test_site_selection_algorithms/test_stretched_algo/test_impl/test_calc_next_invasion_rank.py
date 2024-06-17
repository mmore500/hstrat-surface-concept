import itertools as it

import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.stretched_algo._impl import (
    calc_next_invasion_rank,
)
from hsurf.site_selection_strategy.site_selection_algorithms.tilted_algo._impl import (
    get_hanoi_num_reservations,
)
from pylib import hanoi


@pytest.mark.parametrize("surface_size", [8, 16, 32, 64, 128, 256, 512, 1024])
def test_calc_next_invasion_rank(surface_size: int):
    for rank in range(surface_size, min(2000, 2**surface_size - 1)):
        expected = next(
            ansatz_rank
            for ansatz_rank in it.count(rank + 1)
            if hanoi.get_hanoi_value_incidence_at_index(ansatz_rank)
            < get_hanoi_num_reservations(ansatz_rank, surface_size)
        )
        assert hanoi.get_hanoi_value_at_index(expected) >= 2, (
            expected,
            get_hanoi_num_reservations(expected, surface_size),
            hanoi.get_hanoi_value_incidence_at_index(expected),
        )
        assert expected > rank
        calculated = calc_next_invasion_rank(rank, surface_size)
        assert calculated == expected
