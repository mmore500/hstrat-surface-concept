import itertools as it
import typing

from ..tilted_algo._impl import get_reservation_width_physical
from ._calc_resident_ingest_rank import calc_resident_ingest_rank


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
    num_reservations = surface_size >> 1

    site_counter = it.count()
    for reservation in range(num_reservations):
        width = get_reservation_width_physical(reservation, surface_size)
        for site in it.islice(site_counter, width):
            yield calc_resident_ingest_rank(
                site, surface_size, num_ingests, grip=reservation
            )

    assert next(site_counter) == surface_size
