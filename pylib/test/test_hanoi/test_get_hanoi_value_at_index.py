from pylib.hanoi import get_hanoi_value_at_index


def test_get_hanoi_value():
    # https://oeis.org/A001511
    A001511 = [
        1,
        2,
        1,
        3,
        1,
        2,
        1,
        4,
        1,
        2,
        1,
        3,
        1,
        2,
        1,
        5,
        1,
        2,
        1,
        3,
        1,
        2,
        1,
        4,
        1,
        2,
        1,
        3,
        1,
        2,
        1,
        6,
        1,
        2,
        1,
        3,
        1,
        2,
        1,
        4,
        1,
        2,
        1,
        3,
        1,
        2,
        1,
        5,
        1,
        2,
        1,
        3,
        1,
        2,
        1,
        4,
        1,
        2,
        1,
        3,
        1,
        2,
        1,
        7,
        1,
        2,
        1,
        3,
        1,
        2,
        1,
        4,
        1,
        2,
        1,
        3,
        1,
        2,
        1,
        5,
        1,
        2,
        1,
        3,
        1,
        2,
        1,
        4,
        1,
        2,
        1,
        3,
        1,
        2,
        1,
        6,
        1,
        2,
        1,
        3,
        1,
        2,
        1,
        4,
        1,
    ]

    assert [*map(get_hanoi_value_at_index, range(105))] == [
        x - 1 for x in A001511
    ]
