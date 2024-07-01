from .....pylib import oeis


def calc_tilted_criterion_upper_bound(
    surface_size: int, num_ingests: int
) -> float:
    assert surface_size > 0
    assert num_ingests >= 0
    if num_ingests <= surface_size:
        return 0

    rank = num_ingests - 1
    epoch = rank.bit_length() - surface_size.bit_length() + 1
    assert epoch
    metaepoch = oeis.get_a000325_index_of_value(epoch)
    assert (epoch == 1) == (metaepoch == 1)
    assert (2 <= epoch < 5) == (metaepoch == 2)

    exp = metaepoch - surface_size.bit_length() + 2
    assert exp == (  # previous implementation
        oeis.get_a000295_index_of_value(epoch - 1)
        - surface_size.bit_length()
        + 3
    )

    return 8 * min(  # ??? ansatz
        1 / (2 ** (-min(exp, 0)) - 0.5),
        2 / 1,
    )
