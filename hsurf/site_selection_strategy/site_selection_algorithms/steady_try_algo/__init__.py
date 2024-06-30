"""A steady time stratum ingest algorithm, with non-storage allowed.

See Also
--------
steady_algo :  steady implementation with non-storage disallowed.
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
    "iter_resident_ingest_ranks",
    "iter_retained_ingest_ranks",
    "get_ingest_capacity",
    "has_ingest_capacity",
    "pick_ingest_site",
]
