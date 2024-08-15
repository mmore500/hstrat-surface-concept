import typing


def modpow2(dividend: int, divisor: int) -> int:
    """Perform fast mod using bitwise operations.

    Parameters
    ----------
    dividend : int
        The dividend of the mod operation. Must be a positive integer.
    divisor : int
        The divisor of the mod operation. Must be a positive integer and a
        power of 2.

    Returns
    -------
    int
        The remainder of dividing the dividend by the divisor.
    """
    assert divisor.bit_count() == 1  # Assert divisor is a power of two
    return dividend & (divisor - 1)


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


def tilted_time_lookup(
    S: int, T: int
) -> typing.Iterable[typing.Optional[int]]:
    """Ingest time lookup algorithm for tilted curation.

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
        yield from (v if v < T else None for v in tilted_lookup_impl(S, S))
    else:  # ... assume buffer has been filled
        yield from tilted_lookup_impl(S, T)


def tilted_lookup_impl(S: int, T: int) -> typing.Iterable[int]:
    """Implementation detail for `tilted_time_lookup`."""
    assert T >= S  # T < S redirected to T = S by tilted_time_lookup

    s = S.bit_length() - 1
    t = (T).bit_length() - s  # Current epoch

    blt = t.bit_length()  # Bit length of t
    epsilon_tau = bit_floor(t << 1) > t + blt  # Correction factor
    tau0 = blt - epsilon_tau  # Current meta-epoch
    tau1 = tau0 + 1  # Next meta-epoch
    t0 = (1 << tau0) - tau0  # Opening epoch of current meta-epoch
    T0 = 1 << (t + s - 1)  # Opening time of current epoch

    G_ = S >> tau1 or 1  # Number of invading segments present at current epoch
    w0 = (1 << tau0) - 1  # Smallest segment size at current epoch start
    w1 = (1 << tau1) - 1  # Smallest segment size at next epoch start

    h_ = 0  # Assigned hanoi value of 0th site
    g_p_ = 0  # Calc left-to-right index of 0th segment
    for k in range(S):  # For each site in buffer...
        # Current segment bunch index (i.e., nestedness level)
        b_ = ctz(g_p_ + G_)
        epsilon_w = g_p_ == 0  # Correction factor for segment size
        w = w1 + b_ + epsilon_w  # Number of sites in current segment

        T_ = T
        h = h_
        g_l = (G_ >> (b_ + 1)) + (g_p_ >> (b_ + 1))

        refill_time = T0 + (2 * g_l + 1) * 2**h_ - 1
        invasion_time = (2 * g_l + 1) * 2**h_ - 1

        X_A = h_ >= w - w0 and invasion_time >= T
        X_B = (t - t0 < h < w0) and (t < S - s)
        X_C = (h == t - t0) and (t < S - s) and (refill_time >= T)
        assert X_A + X_B + X_C <= 1

        epsilon_G = G_ * (X_A or X_B or X_C)
        G = G_ + epsilon_G

        if X_A:
            g_l = G_ + g_p_
            T_ = min(bit_floor(invasion_time), T)
            h = h_ - (w - w0)
        elif X_C:
            T_ = bit_floor(refill_time)

        j = (T_ + (1 << h)) >> (h + 1)  # Num seen
        j -= 1

        i = j - modpow2(j - g_l + G, G)

        # Decode ingest time for ith instance of assigned h.v.
        Tbar = ((2 * i + 1) << h) - 1  # True ingest time, Tbar
        yield Tbar

        # Update state for next site...
        h_ += 1  # Assigned h.v. increases within each segment
        g_p_ += h_ == w  # Bump to next segment if current is filled
        h_ *= h_ != w  # Reset h.v. if segment is filled
