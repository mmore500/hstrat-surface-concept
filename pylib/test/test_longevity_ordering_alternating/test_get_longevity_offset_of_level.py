import pylib.longevity_ordering_alternating as loa


def test_get_longevity_offset_of_level():
    assert [
        loa.get_longevity_offset_of_level(level, 1)
        for level in range(1)
    ] == [0]

    assert [
        loa.get_longevity_offset_of_level(level, 2)
        for level in range(2)
    ] == [0, 1]

    assert [
        loa.get_longevity_offset_of_level(level, 4)
        for level in range(3)
    ] == [0, 2, 1]

    assert [
        loa.get_longevity_offset_of_level(level, 8)
        for level in range(4)
    ] == [0, 4, 2, 1]
