import types
import typing

import numpy as np


def sort_differentiae_by_ingest_rank(
    differentiae: typing.Iterable[int],
    num_strata_ingested: int,
    site_selection_algo: types.ModuleType,
) -> typing.List[int]:
    """Sort a collection of differentiae in chronological ingest order.

    This function takes an iterable of differentiae (integers), the number of
    strata that have been ingested, and a module that contains the site
    selection algorithm.

    It returns a list of differentiae sorted by their ingest ranks. If
    multiple founding differentiae (rank 0) are present, only one founding
    differentia will be returned (the longest-lasting founder).

    Parameters
    ----------
    differentiae : typing.Iterable[int]
        Differentiae in order of appearance on a hstrat surface.
    num_strata_ingested : int
        The number of strata that have been ingested onto the surface.
    site_selection_algo : types.ModuleType
        Site selection algorithm.

        Must provide `iter_resident_ingest_ranks`, that yields ingest
        ranks for the given surface size and number of strata ingested.

    Returns
    -------
    typing.List[int]
        A list of differentiae sorted by their ingest ranks, with one
        founding differentia (if any) at the beginning.
    """

    differentiae = [*differentiae]
    surface_size = len(differentiae)
    ingest_ranks = [
        *site_selection_algo.iter_resident_ingest_ranks(
            surface_size, num_strata_ingested
        ),
    ]

    argsort = np.argsort(ingest_ranks, kind="stable")
    sorted_by_rank = [*map(differentiae.__getitem__, argsort)]

    num_founding_sites = ingest_ranks.count(0)
    founder_elimination_order = [
        *site_selection_algo.iter_resident_ingest_ranks(
            surface_size, surface_size
        ),
    ]
    # simplifying assumption about the site selection algorithm
    assert set(founder_elimination_order) == set(range(surface_size))

    longest_founder = founder_elimination_order.index(0)
    # simplifying assumption about the site selection algorithm
    assert longest_founder == 0

    # take at most one founding differentia, the longest-lasting one
    founding_differentiae = sorted_by_rank[:num_founding_sites]
    nonfounding_differentiae = sorted_by_rank[num_founding_sites:]
    return [
        *founding_differentiae[:1],
        *nonfounding_differentiae,
    ]
