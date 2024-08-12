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
    t = max((T + 1).bit_length() - s, 0)  # Current epoch

    # these need to be special-cased anyways
    bunch = 0
    bunch_remaining_segments = 1
    segment_remaining_sites = s
    bunch_complete = True

    for k in range(S - 1):
        segment_size = s - bunch
        bunch_remaining_segments = bunch_remaining_segments or (1 << bunch - 1)
        segment_remaining_sites = segment_remaining_sites or segment_size

        if bunch_complete:
            max_hv = t + segment_size - 1
            hv = max_hv - max_hv % segment_size

        segment = (1 << bunch) - bunch_remaining_segments

        assert hv >= 0, locals()
        assert max_hv >= segment_size
        assert segment_remaining_sites
        segment_remaining_sites -= 1
        bunch_remaining_segments -= not segment_remaining_sites
        hv += not bunch_complete
        hv -= (hv > max_hv) * segment_size
        assert hv >= 0, locals()

        offset = (1 << hv) - 1
        cadence = 1 << (hv + 1)
        res = offset + cadence * segment

        hv_ = hv - (res >= T) * (segment_size)
        assert hv_ >= 0, locals()

        offset_ = (1 << hv_) - 1
        cadence_ = 1 << (hv_ + 1)
        yield offset_ + cadence_ * segment

        bunch_complete = not (
            bunch_remaining_segments or segment_remaining_sites
        )
        bunch += bunch_complete

    yield None
