import functools
import typing

from .stretched_site_selection import (
    stretched_site_selection as site_selection,
)
from .stretched_time_lookup import stretched_time_lookup


def validate_stretched_time_lookup(fn: typing.Callable) -> typing.Callable:
    """Decorator to validate pre- and post-conditions on time lookup."""

    @functools.wraps(fn)
    def wrapper(S: int, T: int) -> typing.Iterable[typing.Optional[int]]:
        assert S.bit_count() == 1  # Assert S is a power of two
        assert 0 <= T  # Assert T is non-negative
        res = fn(S, T)
        for v in res:
            assert v is None or 0 <= v < T  # Assert valid output
            yield v

    return wrapper


time_lookup = validate_stretched_time_lookup(stretched_time_lookup)


def test_stretched_time_lookup_against_site_selection():
    for s in range(1, 12):
        S = 1 << s
        T_max = min(1 << 17 - s, 2**S - 1)
        buffer = [None] * S
        for T in range(T_max):
            actual = time_lookup(S, T)
            assert all(x == y for x, y in zip(buffer, actual))

            site = site_selection(S, T)
            if site is not None:
                buffer[site] = T
