import pylib

def test_get_a030109_value_at_index():
    assert [*map(
        pylib.longevity_ordering_piecewise_ascending.get_a030109_value_at_index,
        range(83),
    )] == [
        # https://oeis.org/A030109
        0,
        0,
        1,
        0,
        2,
        1,
        3,
        0,
        4,
        2,
        6,
        1,
        5,
        3,
        7,
        0,
        8,
        4,
        12,
        2,
        10,
        6,
        14,
        1,
        9,
        5,
        13,
        3,
        11,
        7,
        15,
        0,
        16,
        8,
        24,
        4,
        20,
        12,
        28,
        2,
        18,
        10,
        26,
        6,
        22,
        14,
        30,
        1,
        17,
        9,
        25,
        5,
        21,
        13,
        29,
        3,
        19,
        11,
        27,
        7,
        23,
        15,
        31,
        0,
        32,
        16,
        48,
        8,
        40,
        24,
        56,
        4,
        36,
        20,
        52,
        12,
        44,
        28,
        60,
        2,
        34,
        18,
        50,
    ]
