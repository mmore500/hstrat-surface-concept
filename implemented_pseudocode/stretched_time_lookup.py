import typing


def ctz(x: int) -> int:
    """Count trailing zeros."""
    assert x > 0
    return (x & -x).bit_length() - 1


def bit_floor(n: int) -> int:
    """Calculate the largest power of two not greater than n.

    If zero, returns zero.
    """
    mask = 1 << (n >> 1).bit_length()
    return n & mask


def stretched_time_lookup(
    S: int, T: int
) -> typing.Iterable[typing.Optional[int]]:
    """Ingest time lookup algorithm for stretched curation.

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
    if T < S:  # Patch for before buffer is filled...
        yield from (v if v < T else None for v in stretched_lookup_impl(S, S))
    else:  # ... assume buffer has been filled
        yield from stretched_lookup_impl(S, T)


def stretched_lookup_impl(S: int, T: int) -> typing.Iterable[int]:
    """Implementation detail for `stretched_time_lookup`."""
    assert T >= S  # T < S redirected to T = S by stretched_time_lookup

    s = S.bit_length() - 1
    t = (T).bit_length() - s  # Current epoch

    blt = t.bit_length()  # Bit length of t
    epsilon_tau = bit_floor(t << 1) > t + blt  # Correction factor
    tau0 = blt - epsilon_tau  # Current meta-epoch
    tau1 = tau0 + 1  # Next meta-epoch

    G = S >> tau1 or 1  # Number of invading segments present at current epoch
    w0 = (1 << tau0) - 1  # Smallest segment size at current epoch start
    w1 = (1 << tau1) - 1  # Smallest segment size at current epoch start

    h_ = 0  # Assigned hanoi value of 0th site
    g = 0  # Calc left-to-right index of 0th segment
    for k in range(S):  # For each site in buffer...
        b = ctz(g + G)  # Current segment bunch index (i.e., nestedness level)
        epsilon_w = g == 0  # Correction factor for segment size
        w = w1 + b + epsilon_w  # Number of sites in current segment

        # Determine correction factors for not-yet-seen data items, Tbar_ >= T
        i_ = (G + g) >> (b + 1)  # Guess h.v. incidence (i.e., num seen)
        Tbar_ = ((2 * i_ + 1) << h_) - 1  # Guess ingest time
        epsilon_h_ = (Tbar_ >= T) * (w - w0)  # Correction factor, h
        epsilon_i_ = (Tbar_ >= T) * (g + G - i_)  # Correction factor, i

        # Decode ingest time for ith instance of assigned h.v.
        h = h_ - epsilon_h_  # True hanoi value
        i = i_ + epsilon_i_  # True h.v. incidence
        yield ((2 * i + 1) << h) - 1  # True ingest time, Tbar

        # Update state for next site...
        h_ += 1  # Assigned h.v. increases within each segment
        g += h_ == w  # Bump to next segment if current is filled
        h_ *= h_ != w  # Reset h.v. if segment is filled
