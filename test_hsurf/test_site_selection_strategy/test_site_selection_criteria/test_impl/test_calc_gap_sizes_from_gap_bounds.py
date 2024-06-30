import numpy as np

from hsurf.site_selection_strategy.site_selection_criteria._impl import (
    calc_gap_sizes_from_gap_bounds,
)


def test_empty_gap_bounds():
    result = calc_gap_sizes_from_gap_bounds(np.array([]))
    assert np.array_equal(result, np.array([], dtype=int))


def test_single_gap():
    result = calc_gap_sizes_from_gap_bounds(np.array([0, 5]))
    assert np.array_equal(result, np.array([4]))


def test_multiple_gaps():
    result = calc_gap_sizes_from_gap_bounds(np.array([-1, 1, 3, 6]))
    assert np.array_equal(result, np.array([1, 1, 2]))


def test_zero_size_gaps():
    result = calc_gap_sizes_from_gap_bounds(np.array([0, 1, 2, 3]))
    assert np.array_equal(result, np.array([0, 0, 0]))


def test_mixed_gap_sizes():
    result = calc_gap_sizes_from_gap_bounds(np.array([-1, 0, 3, 4, 8]))
    assert np.array_equal(result, np.array([0, 2, 0, 3]))
