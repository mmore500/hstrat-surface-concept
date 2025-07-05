import numpy as np

from hsurf.site_selection_strategy.site_selection_criteria import (
    calc_gap_sizes,
)


def test_calc_gap_sizes_empty_retained_ranks1():
    result = calc_gap_sizes(np.array([]), 5)
    assert np.array_equal(result, np.array([5]))


def test_calc_gap_sizes_empty_retained_ranks2():
    result = calc_gap_sizes(np.array([]), 0)
    assert np.array_equal(result, np.array([0]))


def test_calc_gap_sizes_single_retained_rank():
    result = calc_gap_sizes(np.array([3]), 5 + 1)
    assert np.array_equal(result, np.array([3, 2]))

    result = calc_gap_sizes(np.array([0]), 1)
    assert np.array_equal(result, np.array([0, 0]))

    result = calc_gap_sizes(np.array([0]), 2)
    assert np.array_equal(result, np.array([0, 1]))


def test_calc_gap_sizes_multiple_retained_ranks():
    result = calc_gap_sizes(np.array([1, 4, 2]), 5 + 1)
    assert np.array_equal(result, np.array([1, 0, 1, 1]))


def test_calc_gap_sizes_all_retained():
    result = calc_gap_sizes(np.array([0, 1, 2, 3]), 3 + 1)
    assert np.array_equal(result, np.array([0, 0, 0, 0, 0]))

    result = calc_gap_sizes(np.array([0, 1, 2, 3]), 5 + 1)
    assert np.array_equal(result, np.array([0, 0, 0, 0, 2]))


def test_calc_gap_sizes_large_gaps():
    result = calc_gap_sizes(np.array([0, 10, 20, 30]), 30 + 1)
    assert np.array_equal(result, np.array([0, 9, 9, 9, 0]))
