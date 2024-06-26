import typing
import warnings

from ._iter_resident_ingest_ranks import iter_resident_ingest_ranks
from ._meta import has_ingest_capacity


def iter_retained_ingest_ranks(
    surface_size: int, num_ingests: int
) -> typing.Iterator[int]:
    """Iterate over retained ingest ranks.

    Differs from `iter_resident_ingest_ranks` in that it excludes surface
    sites that have not yet been explicitly written to.

    Parameters
    ----------
    surface_size : int
        The size of the surface, must be positive power of 2.
    num_ingests : int
        The number of data items that have been ingested, must be non-negative.

    Yields
    ------
    int
        The next retained ingest rank.
    """
    if not has_ingest_capacity(surface_size, num_ingests):
        warnings.warn(
            "Num ingests exceed capacity. Either surface size is not "
            "supported or too many ingestions have elapsed.",
        )
    yield from (
        iter_resident_ingest_ranks(surface_size, num_ingests)
        if num_ingests > surface_size
        else range(num_ingests)
    )
