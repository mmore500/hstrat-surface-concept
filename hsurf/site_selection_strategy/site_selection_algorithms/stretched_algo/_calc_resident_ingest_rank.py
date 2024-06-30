import typing

from ....pylib import hanoi
from ..tilted_algo import calc_resident_ingest_rank as tilted_crdr
from ..tilted_algo._impl import (
    calc_resident_hanoi_value,
    get_epoch_rank,
    get_global_epoch,
    get_grip_reservation_index_logical_at_epoch,
    get_site_genesis_reservation_index_physical,
    get_site_hanoi_value_assigned,
)
from ._pick_ingest_site import pick_ingest_site


def impl_calc_resident_ingest_rank(
    site: int,
    surface_size: int,
    num_ingests: int,
    grip: typing.Optional[int] = None,
) -> int:
    if grip is None:
        grip = get_site_genesis_reservation_index_physical(site, surface_size)

    hanoi_value = calc_resident_hanoi_value(
        site,
        surface_size,
        num_ingests,
        grip=grip,
    )
    assert num_ingests
    rank = num_ingests - 1
    assigned_hanoi_value = get_site_hanoi_value_assigned(
        site, rank, surface_size, grip=grip
    )
    epoch = get_global_epoch(rank, surface_size)
    if hanoi_value != assigned_hanoi_value:
        assert epoch
        epoch -= 1
        rank = get_epoch_rank(epoch, surface_size)
        assert hanoi_value == get_site_hanoi_value_assigned(
            site, rank, surface_size, grip=grip
        )

    reservation = get_grip_reservation_index_logical_at_epoch(
        grip, epoch, surface_size
    )
    res = hanoi.get_index_of_hanoi_value_nth_incidence(
        hanoi_value,
        reservation,
    )
    assert 0 <= res < num_ingests
    return res


def calc_resident_ingest_rank(
    site: int,
    surface_size: int,
    num_ingests: int,
    grip: typing.Optional[int] = None,
) -> int:
    """When `num_ingests` ingest cycles have elapsed, what is the
    ingest rank of the stratum resident at site `site`?

    "grip" stands for genesis reservation index physical of a site. This
    argument may be passed optionally, as an optimization --- i.e., when
    calling via `iter_resident_ingest_ranks`.

    Somewhat (conceptually) inverse to `pick_ingest_site`.

    Returns 0 if the resident stratum traces back to original randomization of
    the surface prior to any algorithm-determined stratum ingests.
    """
    assert surface_size.bit_count() == 1

    if num_ingests <= surface_size:
        return tilted_crdr(site, surface_size, num_ingests, grip=grip)

    rank = num_ingests - 1
    last_site = pick_ingest_site(rank, surface_size)
    if site == last_site:
        return rank

    return impl_calc_resident_ingest_rank(
        site, surface_size, num_ingests, grip=grip
    )
