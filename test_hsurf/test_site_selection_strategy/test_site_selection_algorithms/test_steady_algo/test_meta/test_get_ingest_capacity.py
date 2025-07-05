import opytional as opyt
import pytest

from hsurf.hsurf import steady_algo as algo


@pytest.mark.parametrize("surface_size", range(70))
def test_get_ingest_capacity(surface_size: int):

    res = algo.get_ingest_capacity(surface_size)

    if res != 0:
        algo.pick_ingest_site(0, surface_size)
        algo.pick_ingest_site(opyt.or_value(res, 2**100) - 1, surface_size)
        algo.calc_resident_ingest_rank(0, surface_size, 0)
        algo.calc_resident_ingest_rank(
            0, surface_size, opyt.or_value(res, 2**100) - 1
        )

    if res is not None:
        with pytest.raises(Exception):
            algo.pick_ingest_site(res, surface_size)
