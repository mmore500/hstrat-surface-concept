import itertools as it

from .steady_site_selection import bit_floor, ctz, steady_site_selection


def test_ctz():
    assert ctz(1) == 0
    assert ctz(2) == 1
    assert ctz(3) == 0
    assert ctz(4) == 2
    assert ctz(8) == 3
    assert ctz(16) == 4


def test_bit_floor():
    assert bit_floor(1) == 1
    assert bit_floor(2) == 2
    assert bit_floor(3) == 2
    assert bit_floor(8) == 8
    assert bit_floor(15) == 8


def test_steady_site_selection8():
    actual = (steady_site_selection(8, T) for T in it.count())
    expected = [
        0,  # 0
        1,  # 1
        3,  # 2
        2,  # 3
        5,  # 4
        4,  # 5
        6,  # 6
        0,  # 7
        None,  # 8
        5,  # 9
        None,  # 10
        3,  # 11
        None,  # 12
        6,  # 13
        None,  # 14
        1,  # 15
        None,  # 16
        None,  # 17
        None,  # 18
        5,  # 19
        None,  # 20
        None,  # 21
        None,  # 22
        4,  # 23
        None,  # 24
        None,  # 25
        None,  # 26
        6,  # 27
        None,  # 28
        None,  # 29
        None,  # 30
        2,  # 31
        None,  # 32
        None,  # 33
        None,  # 34
        None,  # 35
        None,  # 36
        None,  # 37
        None,  # 38
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_steady_site_selection16():
    actual = (steady_site_selection(16, T) for T in it.count())
    expected = [
        0,  # 0 --- hv 0
        1,  # 1 --- hv 1
        4,  # 2 --- hv 0
        2,  # 3 --- hv 2
        7,  # 4 --- hv 0
        5,  # 5 --- hv 1
        9,  # 6 --- hv 0
        3,  # 7 --- hv 3
        11,  # 8 --- hv 0
        8,  # 9 --- hv 1
        12,  # 10 --- hv 0
        6,  # 11 --- hv 2
        13,  # 12 --- hv 0
        10,  # 13 --- hv 1
        14,  # 14 --- hv 0
        0,  # 15 --- hv 4
        None,  # 16 --- hv 0
        11,  # 17 --- hv 1
        None,  # 18 --- hv 0
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_steady_site_selection1024():
    actual = {steady_site_selection(1024, T) for T in range(1023)}
    expected = set(range(1023))
    assert actual == expected
