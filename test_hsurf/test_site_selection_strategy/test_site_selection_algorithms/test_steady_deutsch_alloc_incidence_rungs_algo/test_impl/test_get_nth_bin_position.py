import numpy as np
import pytest

from hsurf.site_selection_strategy.site_selection_algorithms.steady_deutsch_alloc_incidence_rungs_algo._impl import (
    get_nth_bin_position,
    get_nth_bin_width,
    get_num_bins,
)


@pytest.mark.parametrize("surface_size", [2**i for i in range(20)])
def test_get_nth_bin_width(surface_size: int):
    bins = [
        get_nth_bin_width(n, surface_size)
        for n in range(get_num_bins(surface_size))
    ]
    assert [
        0,
        *np.cumsum(bins),
    ] == [  # calculate expected positions from widths
        get_nth_bin_position(n, surface_size)
        for n in range(get_num_bins(surface_size) + 1)
    ]
