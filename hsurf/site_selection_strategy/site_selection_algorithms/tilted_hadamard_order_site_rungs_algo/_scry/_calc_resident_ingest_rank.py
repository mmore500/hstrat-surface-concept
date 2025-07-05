import opytional as opyt

from ._impl import (
    calc_rank_of_ingested_hanoi_value,
    calc_resident_hanoi_context,
)


def calc_resident_ingest_rank(
    site: int, surface_size: int, num_ingests: int
) -> int:
    """When `num_ingests` ingest cycles have elapsed, what is the
    ingest rank of the stratum resident at site `site`?

    Somewhat (conceptually) inverse to `pick_ingest_site`.

    Returns 0 if the resident stratum traces back to original randomization of
    the surface prior to any algorithm-determined stratum ingests.
    """
    resident_hanoi_context = calc_resident_hanoi_context(
        site, surface_size, num_ingests
    )
    # candidate_hanoi_value is the hanoi value associated with the
    # ingest resident at site
    # ... use this information to deduce the rank at which the resident
    # ingest at site was ingested
    res = opyt.apply_if_or_value(
        resident_hanoi_context,
        lambda context: calc_rank_of_ingested_hanoi_value(
            context["hanoi value"],
            context["reservation index"],
            surface_size,
            context["focal rank"],
        ),
        0,  # fallback value: no algorithm ingest at site yet
    )
    if num_ingests:
        assert res < num_ingests
    else:
        assert res == 0
    return res
