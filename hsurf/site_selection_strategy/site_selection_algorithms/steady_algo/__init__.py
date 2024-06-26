"""A steady time stratum ingest algorithm.

Categorizes ranks by hanoi values. Divides the surface into bins and waterfalls
successive instances of each hanoi values into each bin from left to right.
Positions within bins rotate in a cycle according to hanoi values.

Bins are arranged into same-capacity segments, with bin size decreasing from
left to right. Bin size decreases by one between each segment. The first two bin
segments have one bin each. The next has two bins, then four, then eight, etc.
The last segment occupies one fourth of the surface with size-one bins.

The rationale behind bin shrink is that at any given time, the number of hanoi
values `v` that have been observed will be twice the number of hanoi values
`v + 1` that have been observed. So, we need bigger bins to hold larger
collections of hanoi values earlier on. This distributional pattern is
self-similar/scale invariant, so the bin distribution is useful indefinitely.

The specific bin distribution used is based on how the initial fill of a surface
fills with hanoi values.

This algorithm could be optimized by looping hanoi values back over for a second
pass on sites that haven't been filled yet once the end of the waterfall is
reached. That bookkeeping is not implemented in this version.
"""

from ._criteria import (
    calc_steady_criterion_exact,
    calc_steady_criterion_lower_bound,
    calc_steady_criterion_upper_bound,
    calc_stretched_criterion_exact,
    calc_stretched_criterion_lower_bound,
    calc_stretched_criterion_upper_bound,
    calc_tilted_criterion_exact,
    calc_tilted_criterion_lower_bound,
    calc_tilted_criterion_upper_bound,
)
from ._enact._pick_ingest_site import pick_ingest_site
from ._meta import get_ingest_capacity, has_ingest_capacity
from ._scry import (
    calc_resident_ingest_rank,
    iter_resident_ingest_ranks,
    iter_retained_ingest_ranks,
)

__all__ = [
    "calc_resident_ingest_rank",
    "calc_steady_criterion_exact",
    "calc_steady_criterion_lower_bound",
    "calc_steady_criterion_upper_bound",
    "calc_stretched_criterion_exact",
    "calc_stretched_criterion_lower_bound",
    "calc_stretched_criterion_upper_bound",
    "calc_tilted_criterion_exact",
    "calc_tilted_criterion_lower_bound",
    "calc_tilted_criterion_upper_bound",
    "get_ingest_capacity",
    "has_ingest_capacity",
    "iter_resident_ingest_ranks",
    "iter_retained_ingest_ranks",
    "pick_ingest_site",
]
