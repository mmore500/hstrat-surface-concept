import typing


def get_first_resolved_resident_rank_inconsistency(
    get_ingest_site_at_rank_impl: typing.Callable,
    get_ingest_rank_at_site_impl: typing.Callable,
    surface_size: int,
    num_generations: int,
    progress_wrap: typing.Callable = lambda x: x,
) -> typing.Optional[typing.Dict]:

    surface_ingest_ranks = [0] * surface_size

    for generation in progress_wrap(range(num_generations)):
        target_site = get_ingest_site_at_rank_impl(
            generation, surface_size
        )
        surface_ingest_ranks[target_site] = generation

        for site in range(surface_size):
            actual_timestamp = surface_ingest_ranks[target_site]
            expected_timestamp = get_ingest_rank_at_site_impl(
                site,
                surface_size,
                generation + 1,
            )
            if actual_timestamp != expected_timestamp:
                return {
                    "actual ingest rank": actual_timestamp,
                    "expected ingest rank": expected_timestamp,
                    "generation": generation + 1,
                    "site": site,
                }

    return None
