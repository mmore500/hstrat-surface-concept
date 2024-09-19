import warnings

from ...steady_algo._meta import has_ingest_capacity

def ctz(x: int) -> int:
    """Count trailing zeros."""
    assert x > 0
    return (x & -x).bit_length() - 1


def bit_floor(x: int) -> int:
    """Return the largest power of two less than or equal to x."""
    assert x > 0
    return 1 << (x.bit_length() - 1)


def pick_ingest_site(rank: int, surface_size: int) -> int:
    """Site selection algorithm for steady curation.

    Parameters
    ----------
    rank : int
        Current logical time.
    surface_size : int
        Buffer size. Must be a power of two.

    Returns
    -------
    int
        Selected site, if any, or surface_size if the item is to be discarded.
    """
    if not has_ingest_capacity(surface_size, rank + 1):
        warnings.warn(
            "Rank exceeds ingest capacity. Either surface size is not "
            "supported or too many ingestions have elapsed.",
        )
    assert surface_size.bit_count() == 1  # assume power of 2 surface size
    # because 0 is special-cased for preservation...
    assert surface_size > 1  # ... need at least somewhere to put ingests

    T = rank
    S = surface_size

    s = S.bit_length() - 1
    t = T.bit_length() - s  # Current epoch (or negative)
    h = ctz(T + 1)  # Current hanoi value
    if h < t:  # If not a top n(T) hanoi value...
        return None  # ...discard without storing

    i = T >> (h + 1)  # Hanoi value incidence (i.e., num seen)
    if i == 0:  # Special case the 0th bunch
        k_b = 0  # Bunch position
        o = 0  # Within-bunch offset
        w = s + 1  # Segment width
    else:
        j = bit_floor(i) - 1  # Num full-bunch segments
        B = j.bit_length()  # Num full bunches
        k_b = (1 << B) * (s - B + 1) - 1  # Bunch position
        w = h - t + 1  # Segment width
        assert w > 0
        o = w * (i - j - 1)  # Within-bunch offset

    p = h % w  # Within-segment offset
    return k_b + o + p  # Calculate placement site
