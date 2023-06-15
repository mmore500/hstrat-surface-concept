import pytest

import pylib


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 1),
        (4, 0),
        (5, 1),
        (6, 2),
        (7, 3),
        (8, 0),
        (9, 1),
        (10, 2),
        (255, 127),
        (256, 0),
        (257, 1),
        (1234567890, 160826066),
    ],
)
def test_bit_drop_msb(input, expected_output):
    assert pylib.bit_drop_msb(input) == expected_output
