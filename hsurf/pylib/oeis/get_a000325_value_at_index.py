# see https://oeis.org/A000295
def get_a000325_value_at_index(n: int) -> int:
    """Return the value of A000325 at the given index.

    A000325(n) = 2^n - n.
    """
    return (1 << n) - n  # Chai Wah Wu, https://oeis.org/A000325
