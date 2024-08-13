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

    b = 0  # Bunch physical index (left-to right)
    b_prime = 1  # Countdown on segments traversed within bunch
    g_prime = s  # Countdown on sites traversed within segment
    b_star = True  # Have traversed all segments in bunch?

    for k in range(S - 1):  # Iterate over buffer sites, except unused last one
        # Calculate info about current segment...
        w = s - b  # Number of sites in current segment (i.e., segment size)
        g = (1 << b) - b_prime  # Overall index of current segment
        h_max = t + w - 1  # Max possible hanoi value in segment during epoch

        # Calculate current hanoi value...
        if b_star:  # Reset h when transitioning between bunches
            h = h_max - h_max % w
        h += not b_star  # Incr h.v. if traversing within bunch
        h -= (h > h_max) * w  # Roll h.v. around back within segment bounds

        # calculating h variant 1
        h0_ = h_max - (h_max % w) + w - g_prime
        h0 = h0_ - w * (h0_ > h_max)
        assert h == h0

        # calculating h variant 2
        i = w - g_prime
        h_max_loc_ = h_max % w
        h_max_loc = h_max_loc_ + (h_max_loc_ < i) * w
        assert h == h_max - (h_max_loc - i)

        # Decode ingest time of assigned h.v. from segment index g, ...
        # ... i.e., how many instances of that h.v. seen before
        T_bar_ = ((g << 1) + 1) * (1 << h) - 1  # Guess ingest time
        epsilon = (T_bar_ >= T) * w  # Correction on h.v. if not yet seen
        T_bar = ((g << 1) + 1) * (1 << (h - epsilon)) - 1  # True ingest time
        yield T_bar

        # Update within-segment state for next site...
        g_prime = g_prime or w
        g_prime -= 1

        # Update within-bunch state for next site...
        b_prime -= not g_prime
        b_star = not (b_prime or g_prime)
        b += b_star
        b_prime = b_prime or (1 << b - 1)
