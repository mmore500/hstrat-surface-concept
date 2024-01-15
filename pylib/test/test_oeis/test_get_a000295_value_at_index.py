import pylib


def test_get_a000295_value_at_index():
    assert [*map(pylib.oeis.get_a000295_value_at_index, range(33))] == [
        # https://oeis.org/A000295/list
        # note: skips zeroth element
        0,
        1,
        4,
        11,
        26,
        57,
        120,
        247,
        502,
        1013,
        2036,
        4083,
        8178,
        16369,
        32752,
        65519,
        131054,
        262125,
        524268,
        1048555,
        2097130,
        4194281,
        8388584,
        16777191,
        33554406,
        67108837,
        134217700,
        268435427,
        536870882,
        1073741793,
        2147483616,
        4294967263,
        8589934558,
    ]
