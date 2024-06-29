"""A steady time stratum deposition algorithm, with non-storage allowed.

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
)
from ._enact._pick_deposition_site import pick_deposition_site
from ._scry._calc_resident_deposition_rank import calc_resident_deposition_rank
from ._scry._iter_resident_deposition_ranks import (
    iter_resident_deposition_ranks,
)
from ._scry._iter_retained_deposition_ranks import (
    iter_retained_deposition_ranks,
)

__all__ = [
    "calc_resident_deposition_rank",
    "calc_steady_criterion_exact",
    "calc_steady_criterion_lower_bound",
    "calc_steady_criterion_upper_bound",
    "calc_stretched_criterion_exact",
    "calc_stretched_criterion_lower_bound",
    "calc_stretched_criterion_upper_bound",
    "iter_resident_deposition_ranks",
    "iter_retained_deposition_ranks",
    "pick_deposition_site",
]
