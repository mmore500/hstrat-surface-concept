import typing

from ._iter_resident_deposition_ranks import iter_resident_deposition_ranks


def iter_retained_deposition_ranks(
    surface_size: int, num_depositions: int
) -> typing.Iterator[int]:
    """Iterate over retained deposition ranks.

    Differs from `iter_resident_deposition_ranks` in that it excludes surface
    sites that have not yet been explicitly written to.

    Parameters
    ----------
    surface_size : int
        The size of the surface, must be positive power of 2.
    num_depositions : int
        The number of data items that have been ingested, must be non-negative.

    Yields
    ------
    int
        The next retained deposition rank.
    """
    yield from (
        iter_resident_deposition_ranks(surface_size, num_depositions)
        if num_depositions > surface_size
        else range(num_depositions)
    )
