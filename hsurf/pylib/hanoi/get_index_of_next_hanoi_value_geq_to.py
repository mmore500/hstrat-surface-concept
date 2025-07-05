from ..fast_pow2_divide import fast_pow2_divide
from .get_hanoi_value_index_cadence import get_hanoi_value_index_cadence


def get_index_of_next_hanoi_value_geq_to(
    value: int,
    index: int,
) -> int:
    """At what index does the next incidence of a given hanoi value greater
    than or equal to `value` occur within the Hanoi sequence past the given
    index?

    Assumes zero-indexing convention. See `get_hanoi_value_at_index` for notes
    on zero-based variant of Hanoi sequence used.
    """
    cadence = get_hanoi_value_index_cadence(value) // 2
    assert cadence

    return fast_pow2_divide(index + cadence + 1, cadence) * cadence - 1
