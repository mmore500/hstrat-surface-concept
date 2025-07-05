import typing

from ..steady_algo import iter_resident_ingest_ranks as steady_impl
from ..tilted_algo import iter_resident_ingest_ranks as tilted_impl


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
    assert surface_size.bit_count() == 1

    for rank in steady_impl(surface_size >> 1, (num_ingests + 1) >> 1):
        yield rank << 1
    for idx, rank in enumerate(
        tilted_impl(surface_size >> 1, num_ingests >> 1)
    ):
        correction = bool(rank) or (idx == 0 and num_ingests >= 2)
        yield (rank << 1) + correction
