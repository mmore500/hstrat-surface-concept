from .....pylib import oeis


def calc_tilted_criterion_upper_bound(
    surface_size: int, num_depositions: int
) -> float:
    assert surface_size > 0
    assert num_depositions >= 0
    if num_depositions <= surface_size:
        return 0

    rank = num_depositions - 1
    epoch = rank.bit_length() - surface_size.bit_length() + 1
    exp = (
        oeis.get_a000295_index_of_value(epoch - 1)
        - surface_size.bit_length()
        + 3
    )
    return min(
        1 / (2 ** (-min(exp, 0)) - 0.5),
        2 / 1,
    )
