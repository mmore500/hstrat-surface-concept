import itertools as it

import pylib


def test_get_a057716_value_at_index():
    expected = [
        # https://oeis.org/A057716
        0,
        3,
        5,
        6,
        7,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        58,
        59,
        60,
        61,
        62,
        63,
        65,
        66,
        67,
        68,
        69,
        70,
        71,
        72,
        73,
        74,
    ]
    assert [
        *map(
            pylib.oeis.get_a057716_value_at_index,
            range(len(expected)),
        )
    ] == expected


def test_get_a057716_value_at_index_generated():

    expected = [
        next(
            it.islice(filter(lambda x: x.bit_count() != 1, it.count()), n, None)
        )
        for n in range(3000)
    ]
    assert [
        *map(
            pylib.oeis.get_a057716_value_at_index,
            range(len(expected)),
        )
    ] == expected
