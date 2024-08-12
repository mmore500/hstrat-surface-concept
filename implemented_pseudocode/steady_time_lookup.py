import typing


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
    if T < S - 1:
        yield from (
            v if v is None or v < T else None
            for v in steady_time_lookup(S, S - 1)
        )
        return

    s = S.bit_length() - 1
    t = (T + 1).bit_length() - s  # Current epoch

    # these need to be special-cased anyways
    bunch = 0
    bunch_remaining_segments = 1
    segment_remaining_sites = s
    bunch_complete = True

    for k in range(S - 1):
        segment_size = s - bunch
        bunch_remaining_segments = bunch_remaining_segments or (1 << bunch - 1)
        segment_remaining_sites = segment_remaining_sites or segment_size
        segment = (1 << bunch) - bunch_remaining_segments

        if bunch_complete:
            max_hv = t + segment_size - 1
            hv = max_hv - max_hv % segment_size

        segment_remaining_sites -= 1
        bunch_remaining_segments -= not segment_remaining_sites
        hv += not bunch_complete
        hv -= (hv > max_hv) * segment_size

        ansatz = ((segment << 1) + 1) * (1 << hv) - 1
        epsilon = (ansatz >= T) * segment_size
        yield ((segment << 1) + 1) * (1 << (hv - epsilon)) - 1

        bunch_complete = not (
            bunch_remaining_segments or segment_remaining_sites
        )
        bunch += bunch_complete

    # last site is never filled
    yield None
