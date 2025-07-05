import itertools as it

import pandas as pd

from hsurf.hsurf import tilted_hadamard_order_site_rungs_algo as algo
from hsurf.pylib import bit_ceil, hanoi
from hsurf.pylib import longevity_ordering_descending as hadamard_order
from hsurf.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._impl import (
    get_num_reservations_provided,
    get_surface_rank_capacity,
)


# helper for test_calc_reservation_reference_incidence
def make_reference_incidence_df(
    surface_size: int, max_generations: int
) -> pd.DataFrame:
    num_generations = min(
        max_generations,
        get_surface_rank_capacity(surface_size) - 1,
    )
    surface_ingest_ranks = [-1] * surface_size
    surface_ingest_incidences = [-1] * surface_size
    surface_hanoi_values = [-1] * surface_size
    surface_ingest_reference_incidences = [-1] * surface_size
    surface_ingest_reference_ranks = [-1] * surface_size

    records = []
    for rank in range(num_generations):
        ingest_hanoi_value = hanoi.get_hanoi_value_at_index(rank)
        target_rank = algo.pick_ingest_site(rank, surface_size)
        surface_hanoi_values[target_rank] = ingest_hanoi_value
        surface_ingest_ranks[target_rank] = rank
        surface_ingest_incidences[
            target_rank
        ] = hanoi.get_hanoi_value_incidence_at_index(rank)
        surface_ingest_reference_ranks[
            target_rank
        ] = surface_ingest_ranks[ingest_hanoi_value]
        surface_ingest_reference_incidences[
            target_rank
        ] = surface_ingest_incidences[ingest_hanoi_value]

        # one row for every site at every rank
        for (
            site,
            site_hanoi_value,
            site_ingest_incidence,
            site_ingest_rank,
            site_ingest_reference_incidence,
            site_ingest_reference_rank,
        ) in zip(
            it.count(),
            surface_hanoi_values,
            surface_ingest_incidences,
            surface_ingest_ranks,
            surface_ingest_reference_incidences,
            surface_ingest_reference_ranks,
        ):
            if site_hanoi_value == -1:
                assert site_ingest_incidence == -1
                assert site_ingest_rank == -1
                assert site_ingest_reference_rank == -1
                continue

            num_reservations_provided = get_num_reservations_provided(
                hanoi_value=site_hanoi_value,
                surface_size=surface_size,
                rank=rank,
            )
            num_chunks = bit_ceil(num_reservations_provided)
            chunk_size = surface_size // num_chunks
            reservation_index = (
                hadamard_order.get_longevity_index_of_mapped_position(
                    site // chunk_size,
                    num_chunks,
                )
            )
            if (
                site % chunk_size != site_hanoi_value
                or reservation_index >= num_reservations_provided
            ):
                continue  # derelict sites, skip

            assert (site < chunk_size) == (reservation_index == 0), {
                "site": site,
                "reservation_index": reservation_index,
            }

            data = {
                "rank": rank,
                "site": site,
                "hanoi value": site_hanoi_value,
                "ingest incidence": site_ingest_incidence,
                "ingest rank": site_ingest_rank,
                "ingest reference incidence": site_ingest_reference_incidence,
                "ingest reference rank": site_ingest_reference_rank,
                "num reservations provided": num_reservations_provided,
                "reservation index": reservation_index,
                "chunk size": chunk_size,
                "num chunks": num_chunks,
            }
            records.append(data)

            assert reservation_index < num_reservations_provided, data

    return pd.DataFrame.from_records(records)
