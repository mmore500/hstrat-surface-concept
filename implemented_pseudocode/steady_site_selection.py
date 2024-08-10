import typing


def ctz(x: int) -> int:
    assert x > 0
    return (x & -x).bit_length() - 1


def bit_floor(x: int) -> int:
    assert x > 0
    return 1 << (x.bit_length() - 1)


def steady_site_selection(S: int, T: int) -> typing.Optional[int]:
    s = S.bit_length() - 1
    t = (T + 1).bit_length() - s
    h = ctz(T + 1)
    if h < t:
        return None

    i = T >> (h + 1)  # hanoi value incidence
    if i == 0:
        w = s  # segment width
        p = h % w  # within-segment offset
        return p

    j = (1 << (i.bit_length() - 1)) - 1  # complete-bunch segments
    b = j.bit_length()  # bunch index minus one
    kb = (1 << b) * (s - b + 1) - 1  # bunch position
    w = h - t + 1  # segment width
    assert w > 0
    o = w * (i - j - 1)  # within-bunch offset
    p = h % w  # within-segment offset
    return kb + o + p
