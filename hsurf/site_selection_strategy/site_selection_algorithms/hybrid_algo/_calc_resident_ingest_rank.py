from ..steady_algo import calc_resident_ingest_rank as steady_impl
from ..tilted_algo import calc_resident_ingest_rank as tilted_impl


def calc_resident_ingest_rank(
    site: int,
    surface_size: int,
    num_ingests: int,
) -> int:
    """When `num_ingests` ingest cycles have elapsed, what is the
    ingest rank of the stratum resident at site `site`?

    "grip" stands for genesis reservation index physical of a site. This
    argument may be passed optionally, as an optimization --- i.e., when
    calling via `iter_resident_ingest_ranks`.

    Somewhat (conceptually) inverse to `pick_ingest_site`.

    Returns 0 if the resident stratum traces back to original randomization of
    the surface prior to any algorithm-determined stratum ingests.
    """
    assert surface_size.bit_count() == 1

    if site < (surface_size >> 1):
        num_ingests += 1
        res = steady_impl(site, surface_size >> 1, num_ingests >> 1)
        return res << 1
    else:
        site -= surface_size >> 1
        res = tilted_impl(site, surface_size >> 1, num_ingests >> 1)
        correction = bool(res) | (site == 0 and num_ingests >= 2)
        return (res << 1) + correction
