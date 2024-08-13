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
    if T < S - 1:  # Patch for before buffer is filled...
        yield from (v if v < T else None for v in steady_lookup_impl(S, S - 1))
    else:  # ... assume buffer has been filled
        yield from steady_lookup_impl(S, T)

    yield None  # Last site is never filled


def steady_lookup_impl(S: int, T: int) -> typing.Iterable[int]:
    """Implementation detail for `steady_time_lookup`."""
    s = S.bit_length() - 1
    t = (T + 1).bit_length() - s  # Current epoch

    # these need to be special-cased anyways
    b = 0  # Bunch physical index (left-to right)
    bunch_remaining_segments = 1
    segment_remaining_sites = s
    bunch_complete = True

    for k in range(S - 1):
        segment_size = s - b
        bunch_remaining_segments = bunch_remaining_segments or (1 << b - 1)
        segment_remaining_sites = segment_remaining_sites or segment_size
        segment = (1 << b) - bunch_remaining_segments

        if bunch_complete:
            h_max = t + segment_size - 1
            h = h_max - h_max % segment_size

        segment_remaining_sites -= 1
        bunch_remaining_segments -= not segment_remaining_sites
        h += not bunch_complete
        h -= (h > h_max) * segment_size

        ansatz = ((segment << 1) + 1) * (1 << h) - 1  # Guess ingest time
        epsilon_T = (ansatz >= T) * segment_size  # Correction if not yet seen
        yield ((segment << 1) + 1) * (1 << (h - epsilon_T)) - 1

        bunch_complete = not (
            bunch_remaining_segments or segment_remaining_sites
        )
        b += bunch_complete
