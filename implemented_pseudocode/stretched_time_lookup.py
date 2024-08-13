import itertools as it
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
    assert tau
    tau0 = tau - 1
    tau1 = tau + 1
    t1 = (1 << tau1) - tau1  # Opening epoch of meta-epoch
    num_segments = S >> (tau + 1)
    min_seglen = 2 ** (tau1) - 1
    min_seglen0 = 2 ** (tau) - 1

    h = 0
    j = 0
    seglen = s + t1

    for k, h in zip(range(seglen), it.count()):
        ansatz = ((2 * j + 1) << h) - 1
        epsilon_h = (ansatz >= T) * (seglen - min_seglen0)
        epsilon_j = (ansatz >= T) * num_segments
        h_prime = h - epsilon_h
        j_prime = j + epsilon_j
        result = ((2 * j_prime + 1) << h_prime) - 1
        assert result < T
        yield result, 0, k

    for g in range(1, num_segments):
        level = ctz(g + num_segments)
        j_base = num_segments >> (level + 1)
        j_level = g >> (level + 1)
        j = j_base + j_level
        seglen = min_seglen + level

        h = 0
        for k, h in zip(range(k + 1, k + seglen + 1), it.count()):
            ansatz = ((2 * j + 1) << h) - 1
            epsilon_h = (ansatz >= T) * (seglen - min_seglen0)
            epsilon_j = (ansatz >= T) * num_segments
            h_prime = h - epsilon_h
            j_prime = j + epsilon_j
            result = ((2 * j_prime + 1) << h_prime) - 1
            assert result < T
            yield result, 0, k, epsilon_h

    print(locals())
    assert k == S - 1, locals()
