import pylib


def test_get_a059893_value_at_index():
    assert [
        *map(
            pylib.longevity_ordering_descending.get_a059893_value_at_index,
            range(71),
        )
    ] == [
        # https://oeis.org/A059893
        1,
        2,
        3,
        4,
        6,
        5,
        7,
        8,
        12,
        10,
        14,
        9,
        13,
        11,
        15,
        16,
        24,
        20,
        28,
        18,
        26,
        22,
        30,
        17,
        25,
        21,
        29,
        19,
        27,
        23,
        31,
        32,
        48,
        40,
        56,
        36,
        52,
        44,
        60,
        34,
        50,
        42,
        58,
        38,
        54,
        46,
        62,
        33,
        49,
        41,
        57,
        37,
        53,
        45,
        61,
        35,
        51,
        43,
        59,
        39,
        55,
        47,
        63,
        64,
        96,
        80,
        112,
        72,
        104,
        88,
        120,
    ]
