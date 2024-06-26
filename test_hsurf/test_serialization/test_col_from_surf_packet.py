import types

from hstrat import hstrat
import numpy as np
import pytest

from hsurf import hsurf


@pytest.mark.parametrize(
    "site_selection_algo, interop_algo",
    [
        (hsurf.hybrid_algo, hsurf.stratum_retention_interop_hybrid_algo),
        (hsurf.steady_algo, hsurf.stratum_retention_interop_steady_algo),
        (hsurf.tilted_algo, hsurf.stratum_retention_interop_tilted_algo),
        (
            hsurf.tilted_sticky_algo,
            hsurf.stratum_retention_interop_tilted_sticky_algo,
        ),
    ],
)
@pytest.mark.parametrize(
    "num_strata_ingested",
    [1, 19, 31, 32, 33, 182],
)
@pytest.mark.parametrize(
    "surface_size",
    [32, 64],
)
def test_col_from_surf_packet_bytes(
    site_selection_algo: types.ModuleType,
    interop_algo: types.ModuleType,
    num_strata_ingested: int,
    surface_size: int,
):
    policy = interop_algo.Policy(surface_size)
    column = hstrat.HereditaryStratigraphicColumn(
        always_store_rank_in_stratum=False,
        stratum_differentia_bit_width=8,
        stratum_retention_policy=policy,
    )
    founding_differentia = column.GetStratumAtColumnIndex(-1).GetDifferentia()
    surface = np.full(surface_size, founding_differentia, dtype=np.uint8)

    for rank in range(1, num_strata_ingested):
        column.DepositStratum()
        site = site_selection_algo.pick_ingest_site(rank, surface_size)
        surface[site] = column.GetStratumAtColumnIndex(-1).GetDifferentia()

    packet = (
        num_strata_ingested.to_bytes(4, byteorder="big", signed=False)
        + surface.tobytes()
    )
    deserialized_column = hsurf.col_from_surf_packet(
        packet=packet,
        differentia_bit_width=8,
        site_selection_algo=site_selection_algo,
    )

    assert (
        column.GetNumStrataDeposited()
        == deserialized_column.GetNumStrataDeposited()
    )
    assert [*deserialized_column.IterRankDifferentiaZip()] == [
        *column.IterRankDifferentiaZip()
    ]

    assert (
        column._always_store_rank_in_stratum
        == deserialized_column._always_store_rank_in_stratum
    )
    assert (
        column._stratum_differentia_bit_width
        == deserialized_column._stratum_differentia_bit_width
    )
    assert (
        column._num_strata_deposited
        == deserialized_column._num_strata_deposited
    )
    assert (
        column._stratum_ordered_store
        == deserialized_column._stratum_ordered_store
    )
    assert (
        column._stratum_retention_policy
        == deserialized_column._stratum_retention_policy
    )

    assert deserialized_column == column
