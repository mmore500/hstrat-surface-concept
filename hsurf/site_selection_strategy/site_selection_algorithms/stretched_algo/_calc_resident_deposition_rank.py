import typing

from ....pylib import hanoi
from ..tilted_algo import calc_resident_deposition_rank as tilted_crdr
from ..tilted_algo._impl import (
    calc_resident_hanoi_value,
    get_grip_reservation_index_logical_at_epoch,
    get_site_genesis_reservation_index_physical,
)
from ._pick_deposition_site import pick_deposition_site


def impl_calc_resident_deposition_rank(
    site: int,
    surface_size: int,
    num_depositions: int,
    grip: typing.Optional[int] = None,
) -> int:
    if grip is None:
        grip = get_site_genesis_reservation_index_physical(site, surface_size)

    hanoi_value = calc_resident_hanoi_value(
        site,
        surface_size,
        num_depositions,
        grip=grip,
    )
    root_site = site - hanoi_value
    grip = get_site_genesis_reservation_index_physical(root_site, surface_size)

    reservation_index = get_grip_reservation_index_logical_at_epoch(
        grip, 0, surface_size
    )

    res = hanoi.get_index_of_hanoi_value_nth_incidence(
        hanoi_value,
        reservation_index,
    )
    assert 0 <= res < num_depositions
    return res


def calc_resident_deposition_rank(
    site: int,
    surface_size: int,
    num_depositions: int,
    grip: typing.Optional[int] = None,
) -> int:
    """When `num_depositions` deposition cycles have elapsed, what is the
    deposition rank of the stratum resident at site `site`?

    "grip" stands for genesis reservation index physical of a site. This
    argument may be passed optionally, as an optimization --- i.e., when
    calling via `iter_resident_deposition_ranks`.

    Somewhat (conceptually) inverse to `pick_deposition_site`.

    Returns 0 if the resident stratum traces back to original randomization of
    the surface prior to any algorithm-determined stratum depositions.
    """
    assert surface_size.bit_count() == 1

    if num_depositions <= surface_size:
        return tilted_crdr(site, surface_size, num_depositions, grip=grip)

    rank = num_depositions - 1
    last_site = pick_deposition_site(rank, surface_size)
    if site == last_site:
        return rank

    return impl_calc_resident_deposition_rank(
        site, surface_size, num_depositions, grip=grip
    )
