import numpy as np
import pytest

from hsurf.site_selection_strategy.site_selection_criteria import (
    calc_stretched_ratios,
)


def test_calc_stretched_ratios_empty():
    result = calc_stretched_ratios(np.array([]), 5)
    assert np.array_equal(result, np.array([]))

    result = calc_stretched_ratios(np.array([]), 0)
    assert np.array_equal(result, np.array([]))


def test_calc_stretched_ratios_single_rank():
    result = calc_stretched_ratios(np.array([3]), 5)
    np.testing.assert_allclose(result, np.array([3 / 1, 2 / 4]), rtol=1e-7)

    result = calc_stretched_ratios(np.array([3]), 3)
    np.testing.assert_allclose(result, np.array([3 / 1, 0 / 4]), rtol=1e-7)

    result = calc_stretched_ratios(np.array([0]), 0)
    np.testing.assert_allclose(result, np.array([0 / 1, 0 / 1]), rtol=1e-7)


def test_calc_stretched_ratios_multiple_ranks():
    result = calc_stretched_ratios(np.array([1, 4, 2]), 5)
    np.testing.assert_allclose(
        result, np.array([1 / 1, 0 / 2, 1 / 3, 1 / 5]), rtol=1e-7
    )


def test_calc_stretched_ratios_zero_rank():
    result = calc_stretched_ratios(np.array([0]), 5)
    np.testing.assert_allclose(result, np.array([0 / 1, 5 / 1]), rtol=1e-7)


def test_calc_stretched_ratios_all_ranks():
    result = calc_stretched_ratios(np.array([0, 1, 2, 3]), 3)
    np.testing.assert_allclose(
        result, np.array([0 / 1, 0 / 2, 0 / 3, 0 / 4, 0 / 4]), rtol=1e-7
    )


def test_calc_stretched_ratios_large_gaps():
    result = calc_stretched_ratios(np.array([0, 10, 20]), 30)
    np.testing.assert_allclose(
        result, np.array([0 / 1, 9 / 1, 9 / 11, 10 / 21]), rtol=1e-7
    )


def test_calc_stretched_ratios_current_rank_zero():
    result = calc_stretched_ratios(np.array([0]), 0)
    np.testing.assert_allclose(result, np.array([0 / 1, 0 / 1]), rtol=1e-7)


@pytest.mark.parametrize(
    "retained_ranks, current_rank",
    [
        (np.array([1, 3, 2]), 5),
        (np.array([0, 1, 2, 3, 4, 5]), 5),
        (np.array([5, 4, 3, 2, 1, 0]), 5),
    ],
)
def test_calc_stretched_ratios_smoke(
    retained_ranks: np.array, current_rank: np.array
):
    result = calc_stretched_ratios(retained_ranks, current_rank)
    assert result.shape == (len(retained_ranks) + 1,)
    assert np.all(result >= 0)
    assert np.all(result <= 1)
