import pylib


def test_get_a000325_value_at_index():
    expected = [
        # note: skips zeroth element
        1,
        2,
        5,
        12,
        27,
        58,
        121,
        248,
        503,
        1014,
        2037,
        4084,
        8179,
        16370,
        32753,
        65520,
        131055,
        262126,
        524269,
        1048556,
        2097131,
        4194282,
        8388585,
        16777192,
        33554407,
        67108838,
        134217701,
        268435428,
        536870883,
        1073741794,
        2147483617,
    ]
    assert expected == [
        *map(pylib.oeis.get_a000325_value_at_index, range(len(expected)))
    ]
