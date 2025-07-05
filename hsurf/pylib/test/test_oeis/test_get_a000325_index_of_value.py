import pylib


def test_get_a000325_value_at_index():
    assert [*map(pylib.oeis.get_a000325_index_of_value, range(1, 16))] == [
        # https://oeis.org/A000325/list
        1,  # 1
        2,  # 2
        2,  # 3
        2,  # 4
        3,  # 5
        3,  # 6
        3,  # 7
        3,  # 8
        3,  # 9
        3,  # 10
        3,  # 11
        4,  # 12
        4,  # 13
        4,  # 14
        4,  # 15
    ]

    for i in range(1, 400):
        n = pylib.oeis.get_a000325_index_of_value(i)
        assert (
            pylib.oeis.get_a000325_value_at_index(n)
            <= i
            < pylib.oeis.get_a000325_value_at_index(n + 1)
        )
