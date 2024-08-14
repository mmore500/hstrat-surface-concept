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
    T0 = 1 << (tau0 + s - 1)  # Opening time of current meta-epoch

    G_ = S >> tau1 or 1  # Number of invading segments present at current epoch
    w0 = (1 << tau0) - 1  # Smallest segment size at current epoch start
    w1 = (1 << tau1) - 1  # Smallest segment size at current epoch start

    h_ = 0  # Assigned hanoi value of 0th site
    g_ = 0  # Calc left-to-right index of 0th segment
    for k in range(S):  # For each site in buffer...
        b = ctz(
            g_ + G_
        )  # Current segment bunch index (i.e., nestedness level)
        epsilon_w = g_ == 0  # Correction factor for segment size
        w = w1 + b + epsilon_w  # Number of sites in current segment

        # Determine correction factors for not-yet-seen data items, Tbar_ >= T
        i_ = (G_ + g_) >> (b + 1)  # Guess h.v. incidence (i.e., num seen)
        Tbar_ = ((2 * i_ + 1) << h_) - 1  # Guess ingest time
        epsilon_h_ = (Tbar_ >= T) * (w - w0)  # Correction factor, h
        epsilon_g_ = (Tbar_ >= T) * (g_ + G_ - i_)  # Correction factor, i
        epsilon_T_ = (Tbar_ >= T) * (T - T0)  # Correction factor, T
        epsilon_G_ = (Tbar_ >= T) * G_

        # Decode ingest time for ith instance of assigned h.v.
        h = h_ - epsilon_h_  # True hanoi value
        assert h >= 0
        g = g_ + epsilon_g_  # True segment index
        G = G_ + epsilon_G_
        Tc = T - epsilon_T_  # Correct to

        # why isnt this Tc - 1?
        j = (Tc + (1 << h)) >> (h + 1)  # Num seen
        assert j
        assert g < j < T
        j -= 1
        if j <= i_ + G:
            G <<= 1  # double back out if haven't made full lap

        front = j - modpow2(j, G)
        ansatz = front + g
        if ansatz > j:
            ansatz -= G

        i = ansatz
        # i = j - o  # True h.v. incidence, WRONG?
        assert 0 <= i <= j
        print(locals())
        yield ((2 * i + 1) << h) - 1  # True ingest time, Tbar

        # Update state for next site...
        h_ += 1  # Assigned h.v. increases within each segment
        g_ += h_ == w  # Bump to next segment if current is filled
        h_ *= h_ != w  # Reset h.v. if segment is filled
