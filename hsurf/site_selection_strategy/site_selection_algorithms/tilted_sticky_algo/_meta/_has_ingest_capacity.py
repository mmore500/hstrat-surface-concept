import math

import opytional as opyt

from ._get_ingest_capacity import get_ingest_capacity


def has_ingest_capacity(surface_size: int, num_ingests: int = 1) -> bool:
    """Does this algorithm have the capacity to ingest `n` data items?

    Parameters
    ----------
    surface_size : int
        The number of buffer sites available.
    num_ingests : int, default 1
        The number of data items hypothetically ingested.

    Returns
    -------
    bool
        True if the algorithm has the capacity to ingest `n` data items.

    See Also
    --------
    get_ingest_capacity : How many data item ingestions does this algorithm
    support?
    """
    assert num_ingests >= 0
    return (
        opyt.or_value(get_ingest_capacity(surface_size), math.inf)
        >= num_ingests
    )
