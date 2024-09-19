import itertools as it
import warnings

from ._iter_resident_ingest_ranks import iter_resident_ingest_ranks


def calc_resident_ingest_rank(
    site: int, surface_size: int, num_ingests: int
) -> int:
    """When `num_ingests` ingest cycles have elapsed, what is the
    ingest rank of the stratum resident at site `site`?

    Somewhat (conceptually) inverse to `pick_ingest_site`.

    Returns 0 if the resident stratum traces back to original randomization of
    the surface prior to any algorithm-determined stratum ingests.
    """
    if not has_ingest_capacity(surface_size, num_ingests):
        warnings.warn(
            "Num ingests exceed capacity. Either surface size is not "
            "supported or too many ingestions have elapsed.",
        )
    gen = iter_resident_ingest_ranks(surface_size, num_ingests)
    next(it.islice(gen, site, None))