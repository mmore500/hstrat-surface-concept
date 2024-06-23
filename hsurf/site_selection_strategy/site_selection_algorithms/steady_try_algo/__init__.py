"""A steady time stratum deposition algorithm, with non-storage allowed.

See Also
--------
steady_algo :  steady implementation with non-storage disallowed.
"""

from ._enact._pick_deposition_site import pick_deposition_site
from ._scry._calc_resident_deposition_rank import calc_resident_deposition_rank
from ._scry._iter_resident_deposition_ranks import (
    iter_resident_deposition_ranks,
)

__all__ = [
    "calc_resident_deposition_rank",
    "iter_resident_deposition_ranks",
    "pick_deposition_site",
]
