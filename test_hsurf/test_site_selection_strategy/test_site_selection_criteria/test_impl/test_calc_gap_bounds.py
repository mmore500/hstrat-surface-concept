import numpy as np

from hsurf.site_selection_strategy.site_selection_criteria._impl import (
    calc_gap_bounds,
)


def test_calc_gap_bounds_empty_retained_ranks1():
    retained_ranks = np.array([])
    current_rank = 5
    result = calc_gap_bounds(retained_ranks, current_rank + 1)
    expected = np.array([-1, 6], dtype=int)
    assert np.array_equal(result, expected)


def test_calc_gap_bounds_empty_retained_ranks2():
    retained_ranks = np.array([])
    result = calc_gap_bounds(retained_ranks, 0)
    expected = np.array([-1, 0], dtype=int)
    assert np.array_equal(result, expected)


def test_calc_gap_bounds_single_element():
    retained_ranks = np.array([3])
    current_rank = 5
    result = calc_gap_bounds(retained_ranks, current_rank + 1)
    expected = np.array([-1, 3, 6])
    assert np.array_equal(result, expected)


def test_calc_gap_bounds_multiple_elements():
    retained_ranks = np.array([5, 2, 7])
    current_rank = 8
    result = calc_gap_bounds(retained_ranks, current_rank + 1)
    expected = np.array([-1, 2, 5, 7, 9])
    assert np.array_equal(result, expected)


def test_calc_gap_bounds_current_rank_zero():
    retained_ranks = np.array([1, 4, 6])
    current_rank = 10
    result = calc_gap_bounds(retained_ranks, current_rank + 1)
    expected = np.array([-1, 1, 4, 6, 11])
    assert np.array_equal(result, expected)


def test_calc_gap_bounds_singleton_zero():
    retained_ranks = np.array([0])
    current_rank = 0
    result = calc_gap_bounds(retained_ranks, current_rank + 1)
    expected = np.array([-1, 0, 1])
    assert np.array_equal(result, expected)
