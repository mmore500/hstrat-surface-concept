import warnings

from .._enact import pick_ingest_site
from .._impl import (
    calc_resident_ingest_rank_wrt_bin,
    get_bin_number_of_position,
    get_nth_bin_position,
)
from .._meta import has_ingest_capacity


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

    if num_ingests == 0:
        return 0

    # handle chaff, a.k.a., ingests placed onto the surface for expired
    # hanoi values using lookahead to next unexpired hanoi value
    if site == pick_ingest_site(num_ingests - 1, surface_size):
        return num_ingests - 1

    if site == 0:  # handle special-cased position zero
        return 0
    site -= 1  # handle special-cased position zero

    bin_number = get_bin_number_of_position(site, surface_size)
    within_bin_index = site - get_nth_bin_position(bin_number, surface_size)

    return calc_resident_ingest_rank_wrt_bin(
        bin_number, within_bin_index, num_ingests, surface_size
    )
