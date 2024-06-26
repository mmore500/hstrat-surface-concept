import typing

from ..hanoi import get_hanoi_value_at_index


def get_first_decreasing_hanoi_value_ingest(
    get_ingest_site_at_rank_impl: typing.Callable,
    surface_size: int,
    num_generations: int,
    progress_wrap: typing.Callable = lambda x: x,
) -> typing.Optional[typing.Dict]:

    surface_hanoi_values = [-1] * surface_size
    for rank in progress_wrap(range(num_generations)):
        target_site = get_ingest_site_at_rank_impl(rank, surface_size)
        ingested_hanoi_value = get_hanoi_value_at_index(rank)
        resident_hanoi_value = surface_hanoi_values[target_site]
        if ingested_hanoi_value < resident_hanoi_value:
            return {
                "ingested hanoi value": ingested_hanoi_value,
                "resident hanoi value": resident_hanoi_value,
                "rank": rank,
                "surface size": surface_size,
                "target site": target_site,
            }

    return None
