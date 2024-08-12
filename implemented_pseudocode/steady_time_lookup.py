import itertools as it
import typing

from .hsurf import hsurf


def steady_time_lookup(
    S: int, T: int
) -> typing.Iterable[typing.Optional[int]]:
    """Ingest time lookup algorithm for steady curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : int
        Current logical time.

    Returns
    -------
    typing.Optional[int]
        Ingest time, if any.
    """
    iter_ = hsurf.steady_try_algo.iter_resident_ingest_ranks(S, T)
    next(iter_)  # Skip the first value
    first = next(iter_)
    yield first if T else None
    yield from (v or None for v in iter_)
    yield None  # Last site never written to
