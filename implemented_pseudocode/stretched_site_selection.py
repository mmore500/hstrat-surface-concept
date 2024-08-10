import typing

from .hsurf import hsurf


def stretched_site_selection(S: int, T: int) -> typing.Optional[int]:
    """Site selection algorithm for stretched curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : int
        Current logical time. Must be less than 2**S - 1.

    Returns
    -------
    typing.Optional[int]
        Selected site, if any.
    """
    res = hsurf.stretched_try_algo.pick_ingest_site(T, S)
    return None if res == S else res
