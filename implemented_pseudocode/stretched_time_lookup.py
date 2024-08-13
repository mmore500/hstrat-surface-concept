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
    assert T >= S

    s = S.bit_length() - 1
    t = (T).bit_length() - s  # Current epoch

    blt = t.bit_length()  # Bit length of t
    epsilon_tau = bit_floor(t << 1) > t + blt  # Correction factor
    tau = blt - epsilon_tau  # Current meta-epoch
    t0 = (1 << tau) - tau  # Opening epoch of meta-epoch
    invasions = t - t0
    # b = S >> (tau + 1) or 1  # Num bunches available to h.v.

    # special-case 0th
    # ansatz = (1 << s + t - 1) - 1
    # epsilon = ansatz >= T
    # for k in range(s + t - epsilon):
    #     yield (1 << k) - 1
    # ansatz = (1 << s + t - 1) - 1
    # epsilon = ansatz >= T
    for k in range(s + t0):
        yield 0
        # yield (1 << k) - 1

    print(k)
    assert tau
    tau0 = tau - 1
    num_segments = S >> (tau0 + 1)
    min_seglen = 2 ** (tau) - 1

    for g in range(1, num_segments):
        level = ctz(g + num_segments)
        seglen = min_seglen + level
        print(g, min_seglen, seglen)

        for k in range(k, k + seglen + 1):
            yield g

    assert k == S - 1, locals()
