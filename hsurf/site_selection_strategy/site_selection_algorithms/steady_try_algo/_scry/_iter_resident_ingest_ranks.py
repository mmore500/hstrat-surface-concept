import typing

from ...steady_algo._impl import (
    calc_resident_ingest_rank_wrt_bin,
    iter_bin_coords,
)


def iter_resident_ingest_ranks(
    surface_size: int, num_ingests: int
) -> typing.Iterable[int]:
    """When `num_ingests` ingest cycles have elapsed, what is the
    ingest rank of the stratum resident at each site?

    Yields ingest ranks in order of site index, from site 0 up to site
    `surface_size`. Returns 0 if the resident stratum traces back to original
    randomization of the surface prior to any algorithm-determined stratum
    ingests.

    Somewhat (conceptually) inverse to `pick_ingest_site`.
    """

    if surface_size:
        yield 0

    yield from (
        calc_resident_ingest_rank_wrt_bin(
            bin_number, within_bin_index, num_ingests, surface_size
        )
        for bin_number, within_bin_index in iter_bin_coords(surface_size)
    )
