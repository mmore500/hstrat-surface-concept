import numpy as np
import pytest

from hsurf.site_selection_strategy.site_selection_bounds import (
    optimize_criterion,
)
from hsurf.site_selection_strategy.site_selection_bounds._impl import (
    calc_gap_ratio_lower_bound,
)


def _stretched_criterion(a: int, b: int) -> float:
    res = (b - a - 1) / max(a + 1, 1)
    assert np.isfinite(res)
    return res


@pytest.mark.parametrize("surface_size", range(1, 10))
@pytest.mark.parametrize("rank", range(100))
def test_against_optimized_criterion_small(surface_size: int, rank: int):
    if rank >= 2**surface_size:
        return

    optimized_value = optimize_criterion(
        rank, surface_size, _stretched_criterion
    )
    calculated_value = calc_gap_ratio_lower_bound(rank, surface_size)
    assert np.isfinite(calculated_value)
    assert calculated_value >= 0.0

    assert (
        optimized_value >= calculated_value
        or pytest.approx(optimized_value) == calculated_value
    )


@pytest.mark.heavy
@pytest.mark.parametrize("surface_size", [100, 127, 128])
@pytest.mark.parametrize("rank", [0, 1, 1023, 1024, 400, 511, 512])
def test_against_optimized_criterion_large(surface_size: int, rank: int):
    optimized_value = optimize_criterion(
        rank, surface_size, _stretched_criterion
    )
    calculated_value = calc_gap_ratio_lower_bound(rank, surface_size)
    assert np.isfinite(calculated_value)
    assert calculated_value >= 0.0

    assert (
        optimized_value >= calculated_value
        or pytest.approx(optimized_value) == calculated_value
    )
