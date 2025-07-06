import typing
import warnings

from ..tilted_algo import (
    calc_resident_ingest_rank as impl_calc_resident_ingest_rank,
)
from ._meta import has_ingest_capacity
from ._pick_ingest_site import pick_ingest_site


def calc_resident_ingest_rank(
    site: int,
    surface_size: int,
    num_ingests: int,
    grip: typing.Optional[int] = None,
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
    if not has_ingest_capacity(surface_size, num_ingests):
        warnings.warn(
            "Num ingests exceed capacity. Either surface size is not "
            "supported or too many ingestions have elapsed.",
        )

    if num_ingests == 0:
        return 0

    assert surface_size.bit_count() == 1

    rank = num_ingests - 1

    if site == 0:
        return 0

    last_site = pick_ingest_site(rank, surface_size)
    if site == last_site:
        return rank

    return impl_calc_resident_ingest_rank(
        site, surface_size, num_ingests, grip=grip
    )
