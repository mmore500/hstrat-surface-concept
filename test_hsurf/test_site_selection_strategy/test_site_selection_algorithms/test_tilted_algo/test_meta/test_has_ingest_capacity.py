import opytional as opyt
import pytest

from hsurf.hsurf import tilted_algo as algo


@pytest.mark.parametrize("surface_size", range(70))
def test_get_ingest_capacity(surface_size: int):

    capacity = algo.get_ingest_capacity(surface_size)

    if capacity != 0:
        assert algo.has_ingest_capacity(surface_size, 0)
        assert algo.has_ingest_capacity(
            surface_size, opyt.or_value(capacity, 2**100)
        )

    if capacity is not None:
        assert not algo.has_ingest_capacity(surface_size, capacity + 1)
