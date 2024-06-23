import typing

from ...steady_algo._impl import (
    calc_resident_deposition_rank_wrt_bin,
    iter_bin_coords,
)


def iter_resident_deposition_ranks(
    surface_size: int, num_depositions: int
) -> typing.Iterable[int]:
    """When `num_depositions` deposition cycles have elapsed, what is the
    deposition rank of the stratum resident at each site?

    Yields deposition ranks in order of site index, from site 0 up to site
    `surface_size`. Returns 0 if the resident stratum traces back to original
    randomization of the surface prior to any algorithm-determined stratum
    depositions.

    Somewhat (conceptually) inverse to `pick_deposition_site`.
    """

    if surface_size:
        yield 0

    yield from (
        calc_resident_deposition_rank_wrt_bin(
            bin_number, within_bin_index, num_depositions, surface_size
        )
        for bin_number, within_bin_index in iter_bin_coords(surface_size)
    )
