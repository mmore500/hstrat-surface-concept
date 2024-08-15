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
    g_p = 0  # Left-to-right (physical) segment index
    for k in range(S):  # For each site in buffer...
        b_l = ctz(G_ + g_p)  # Reverse fill order (logical) bunch index
        epsilon_w = g_p == 0  # Correction factor for segment size
        w = w1 + b_l + epsilon_w  # Number of sites in current segment
        g_l_ = (G_ + g_p) >> (b_l + 1)  # Logical (fill order) segment index

        # Detect scenario...
        # Scenario A: site in invaded segment, h.v. ring buffer intact
        X_A = h_ - (t - t0) > w - w0  # To be invaded in future epoch t in tau?
        T_i = (2 * g_l_ + 1) * (1 << h_) - 1  # When overwritten by invader?
        X_A_ = h_ - (t - t0) == w - w0 and T_i >= T  # To be invaded this epoch?

        # Scenario A: site in invading segment, h.v. ring buffer intact
        X_B = (t - t0 < h_ < w0) and (t < S - s)  # At future epoch t in tau?
        T_r = T0 + T_i  # When site refilled after ring buffer halves?
        X_B_ = (h_ == t - t0) and (t < S - s) and (T_r >= T)  # At this epoch?

        # note that scenarios are mutually exclusive
        assert X_A + X_A_ + X_B + X_B_ <= 1

        # Calculate corrected values...
        epsilon_G = (X_A or X_A_ or X_B or X_B_) * G_
        epsilon_h = (X_A or X_A_) * (w - w0)
        T0_i = bit_floor(T_i)  # Opening time of epoch when invaded
        T0_r = bit_floor(T_r)  # Opening time of epoch when refilled
        epsilon_T = X_A_ * (T - T0_i) + X_B_ * (T - T0_r)

        G = G_ + epsilon_G
        h = h_ - epsilon_h
        Tc = T - epsilon_T  # Corrected time
        g_l = (X_A or X_A_) * (G_ + g_p) or g_l_

        # Decode what h.v. instance fell on site k...
        j = ((Tc + (1 << h)) >> (h + 1)) - 1  # Num seen, less one
        i = j - modpow2(j - g_l + G, G)  # H.v. incidence resident at site k
        # ... then decode ingest time for that ith h.v. instance
        yield ((2 * i + 1) << h) - 1  # True ingest time, Tbar

        # Update state for next site...
        h_ += 1  # Assigned h.v. increases within each segment
        g_p += h_ == w  # Bump to next segment if current is filled
        h_ *= h_ != w  # Reset h.v. if segment is filled
