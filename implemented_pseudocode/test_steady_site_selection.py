# fmt: off
import itertools as it

from .steady_site_selection import bit_floor, ctz, steady_site_selection


def test_ctz():
    assert [*map(ctz, range(1, 17))] == [
        0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 4
    ]


def test_bit_floor():
    assert [*map(bit_floor, range(1, 17))] == [
        1, 2, 2, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 16
    ]


def test_steady_site_selection8():
    actual = (steady_site_selection(8, T) for T in it.count())
    expected = [
        0, 1, 3, 2, 5, 4, 6, 0,  # 0-7
        None, 5, None, 3, None, 6, None, 1,  # 8-15
        None, None, None, 5, None, None, None, 4,  # 16-23
        None, None, None, 6, None, None, None, 2,  # 24-31
        None, None, None, None, None, None, None, 5 # 32-39
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_steady_site_selection16():
    actual = (steady_site_selection(16, T) for T in it.count())
    expected = [
        0, 1, 4, 2, 7, 5, 9, 3,  # 0-7 --- hv 0,1,0,2,0,1,0,3
        11, 8, 12, 6, 13, 10, 14, 0,  # 8-15 --- hv 0,1,0,2,0,1,0,4
        None, 11, None  # 16-18 --- hv 0,1,0
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_steady_site_selection1024():
    actual = {steady_site_selection(1024, T) for T in range(1023)}
    expected = set(range(1023))
    assert actual == expected
