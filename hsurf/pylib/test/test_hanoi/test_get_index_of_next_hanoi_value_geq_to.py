import itertools as it

import pytest

from pylib.hanoi import (
    get_hanoi_value_at_index,
    get_index_of_next_hanoi_value_geq_to,
)


@pytest.mark.parametrize("hanoi_value", range(1, 6))
@pytest.mark.parametrize("i", range(1000))
def test_get_index_of_next_hanoi_value_geq_to(hanoi_value: int, i: int):
    expected = next(
        filter(
            lambda n: get_hanoi_value_at_index(n) >= hanoi_value,
            it.count(i + 1),
        )
    )
    assert expected == get_index_of_next_hanoi_value_geq_to(hanoi_value, i)
