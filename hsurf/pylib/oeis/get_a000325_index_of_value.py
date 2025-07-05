from .get_a000325_value_at_index import get_a000325_value_at_index


# see https://oeis.org/A000325
def get_a000325_index_of_value(v: int) -> int:
    """Return the greatest index of A000325 with value `<= v`.

    v must be positive.
    """
    assert v > 0
    ansatz = (v).bit_length()
    correction = get_a000325_value_at_index(ansatz) > v
    return ansatz - correction
