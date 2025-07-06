"""Transplanted from
`05-fractional-incrementing-incidence-reservation-surface-with-safety-aligned-transition.ipynb`"""

from ._enact import pick_ingest_site
from ._scry import calc_resident_ingest_rank, iter_resident_ingest_ranks

__all__ = [
    "calc_resident_ingest_rank",
    "iter_resident_ingest_ranks",
    "pick_ingest_site",
]
