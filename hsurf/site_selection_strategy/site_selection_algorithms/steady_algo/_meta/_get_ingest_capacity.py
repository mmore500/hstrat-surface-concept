import typing


def get_ingest_capacity(surface_size: int) -> typing.Optional[int]:
    """How many data item ingestions does this algorithm support?

    Returns None if the number of supported ingestions cannot be represented
    (e.g., unlimited).

    See Also
    --------
    has_ingest_capacity : Does this algorithm have the capacity to ingest `n`
    data items?
    """
    surface_size_ok = surface_size.bit_count() == 1 and surface_size > 1
    return None if surface_size_ok else 0
