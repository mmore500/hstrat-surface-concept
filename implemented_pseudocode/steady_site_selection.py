import typing


def ctz(x: int) -> int:
    """Count trailing zeros."""
    assert x > 0
    return (x & -x).bit_length() - 1


def bit_floor(x: int) -> int:
    """Return the largest power of two less than or equal to x."""
    assert x > 0
    return 1 << (x.bit_length() - 1)


def steady_site_selection(S: int, T: int) -> typing.Optional[int]:
    """Site selection algorithm for steady curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : int
        Current logical time.

    Returns
    -------
    typing.Optional[int]
        Selected site, if any.
    """
    s = S.bit_length() - 1
    t = (T + 1).bit_length() - s  # Current epoch (or negative)
    h = ctz(T + 1)  # Current hanoi value
    if h < t:  # If not a top n(T) hanoi value...
        return None  # ...discard without storing

    i = T >> (h + 1)  # Hanoi value incidence
    if i == 0:  # Special case the 0th bunch
        k = 0  # Bunch position
        o = 0  # Within-bunch offset
        w = s  # Segment width
    else:
        j = bit_floor(i) - 1  # Num full-bunch segments
        b = j.bit_length()  # Num full bunches
        k = (1 << b) * (s - b + 1) - 1  # Bunch position
        w = h - t + 1  # Segment width
        assert w > 0
        o = w * (i - j - 1)  # Within-bunch offset

    p = h % w  # Within-segment offset
    return k + o + p  # Calculate placement site
