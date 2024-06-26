import math
import types

from hstrat import hstrat
import opytional as opyt
import pytest

from hsurf import hsurf


@pytest.mark.parametrize(
    "interop_algo",
    [
        hsurf.stratum_retention_interop_hybrid_algo,
        hsurf.stratum_retention_interop_steady_algo,
        hsurf.stratum_retention_interop_stretched_algo,
        hsurf.stratum_retention_interop_tilted_algo,
        hsurf.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_GenDropRanks(interop_algo: types.ModuleType, surface_size: int):
    policy = interop_algo.Policy(surface_size)

    for rank in range(surface_size):
        assert [*policy.GenDropRanks(rank)] == []

    # hybrid algo needs tighter bound than others
    nrank = min(
        100,
        opyt.or_value(
            policy._policy_spec._site_selection_algo.get_ingest_capacity(
                surface_size,
            ),
            math.inf,
        ),
    )
    for rank in range(surface_size, nrank):
        site = interop_algo._site_selection_algo.pick_ingest_site(
            rank, surface_size
        )
        assert [*policy.GenDropRanks(rank)] == [
            interop_algo._site_selection_algo.calc_resident_ingest_rank(
                site, surface_size, rank
            )
        ]


@pytest.mark.parametrize(
    "interop_algo",
    [
        hsurf.stratum_retention_interop_hybrid_algo,
        hsurf.stratum_retention_interop_steady_algo,
        hsurf.stratum_retention_interop_stretched_algo,
        hsurf.stratum_retention_interop_tilted_algo,
        hsurf.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_CalcNumStrataRetainedExact(
    interop_algo: types.ModuleType, surface_size: int
):
    policy = interop_algo.Policy(surface_size)
    nrank = min(
        100,
        opyt.or_value(
            policy._policy_spec._site_selection_algo.get_ingest_capacity(
                surface_size,
            ),
            math.inf,
        ),
    )

    for rank in range(nrank):
        assert policy.CalcNumStrataRetainedExact(rank) == min(
            rank, surface_size
        )


@pytest.mark.parametrize(
    "interop_algo",
    [
        hsurf.stratum_retention_interop_hybrid_algo,
        hsurf.stratum_retention_interop_steady_algo,
        hsurf.stratum_retention_interop_stretched_algo,
        hsurf.stratum_retention_interop_tilted_algo,
        hsurf.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_CalcRankAtColumnIndex(
    interop_algo: types.ModuleType, surface_size: int
):
    policy = interop_algo.Policy(surface_size)
    nrank = min(
        100,
        opyt.or_value(
            policy._policy_spec._site_selection_algo.get_ingest_capacity(
                surface_size,
            ),
            math.inf,
        ),
    )

    assert policy.CalcNumStrataRetainedExact(0) == 0
    for rank in range(1, nrank):
        column_ranks = [
            policy.CalcRankAtColumnIndex(index, rank)
            for index in range(policy.CalcNumStrataRetainedExact(rank))
        ]
        assert column_ranks == sorted(
            set(  # have to deduplicate rank 0 entries
                interop_algo._site_selection_algo.iter_resident_ingest_ranks(
                    surface_size, rank
                ),
            ),
        )


@pytest.mark.parametrize(
    "interop_algo",
    [
        hsurf.stratum_retention_interop_hybrid_algo,
        hsurf.stratum_retention_interop_steady_algo,
        hsurf.stratum_retention_interop_stretched_algo,
        hsurf.stratum_retention_interop_tilted_algo,
        hsurf.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_CalcNumStrataRetainedUpperBound(
    interop_algo: types.ModuleType, surface_size: int
):
    policy = interop_algo.Policy(surface_size)
    nrank = min(
        100,
        opyt.or_value(
            policy._policy_spec._site_selection_algo.get_ingest_capacity(
                surface_size,
            ),
            math.inf,
        ),
    )

    for rank in range(nrank):
        assert policy.CalcNumStrataRetainedExact(
            rank
        ) <= policy.CalcNumStrataRetainedUpperBound(rank)


@pytest.mark.parametrize(
    "interop_algo",
    [
        hsurf.stratum_retention_interop_hybrid_algo,
        hsurf.stratum_retention_interop_steady_algo,
        hsurf.stratum_retention_interop_stretched_algo,
        hsurf.stratum_retention_interop_tilted_algo,
        hsurf.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_IterRetainedRanks(interop_algo: types.ModuleType, surface_size: int):
    policy = interop_algo.Policy(surface_size)
    nrank = min(
        100,
        opyt.or_value(
            policy._policy_spec._site_selection_algo.get_ingest_capacity(
                surface_size,
            ),
            math.inf,
        ),
    )

    assert [*policy.IterRetainedRanks(0)] == []
    for rank in range(1, nrank):
        column_ranks = [*policy.IterRetainedRanks(rank)]
        assert column_ranks == sorted(
            set(  # have to deduplicate rank 0 entries
                interop_algo._site_selection_algo.iter_resident_ingest_ranks(
                    surface_size, rank
                ),
            ),
        )


@pytest.mark.parametrize(
    "interop_algo",
    [
        hsurf.stratum_retention_interop_hybrid_algo,
        hsurf.stratum_retention_interop_steady_algo,
        hsurf.stratum_retention_interop_stretched_algo,
        hsurf.stratum_retention_interop_tilted_algo,
        hsurf.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_hstrat_test_drive_integration(
    interop_algo: types.ModuleType, surface_size: int
):
    population_size = 1024
    num_generations = min(
        100,
        opyt.or_value(
            interop_algo.Policy(
                surface_size
            )._policy_spec._site_selection_algo.get_ingest_capacity(
                surface_size,
            ),
            math.inf,
        ),
    )
    alife_df = hstrat.evolve_fitness_trait_population(
        num_islands=4,
        num_niches=4,
        num_generations=num_generations,
        population_size=population_size,
        tournament_size=1,
    )

    extant_population = hstrat.descend_template_phylogeny_alifestd(
        alife_df,
        seed_column=hstrat.HereditaryStratigraphicColumn(
            interop_algo.Policy(surface_size)
        ),
    )
    assert len(extant_population) == population_size
    assert all(
        c.GetNumStrataDeposited() == num_generations + 2
        for c in extant_population
    )


@pytest.mark.parametrize(
    "always_store_rank_in_stratum",
    [True, False],
)
@pytest.mark.parametrize(
    "interop_algo",
    [
        hsurf.stratum_retention_interop_hybrid_algo,
        hsurf.stratum_retention_interop_steady_algo,
        hsurf.stratum_retention_interop_stretched_algo,
        hsurf.stratum_retention_interop_tilted_algo,
        hsurf.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 32, 64],
)
def test_hstrat_column_integration(
    always_store_rank_in_stratum: bool,
    interop_algo: types.ModuleType,
    surface_size: int,
):
    column = hstrat.HereditaryStratigraphicColumn(
        always_store_rank_in_stratum=always_store_rank_in_stratum,
        stratum_differentia_bit_width=8,
        stratum_retention_policy=interop_algo.Policy(surface_size),
    )
    policy = column._stratum_retention_policy
    ssa = policy.GetSpec()._site_selection_algo
    nrank = min(
        100,
        opyt.or_value(
            policy._policy_spec._site_selection_algo.get_ingest_capacity(
                surface_size,
            ),
            math.inf,
        ),
    )
    for g in range(nrank - 1):
        assert set(column.IterRetainedRanks()) == set(
            ssa.iter_resident_ingest_ranks(surface_size, g + 1),
        )
        column.DepositStratum()


def test_eq():
    assert hsurf.stratum_retention_interop_hybrid_algo.Policy(
        8
    ) != hsurf.stratum_retention_interop_hybrid_algo.Policy(16)

    assert hsurf.stratum_retention_interop_hybrid_algo.Policy(
        8
    ) == hsurf.stratum_retention_interop_hybrid_algo.Policy(8)

    assert hsurf.stratum_retention_interop_tilted_sticky_algo.Policy(
        8
    ) != hsurf.stratum_retention_interop_hybrid_algo.Policy(8)

    assert hsurf.stratum_retention_interop_tilted_algo.Policy(
        64
    ) == hsurf.stratum_retention_interop_tilted_algo.Policy(64)

    policy = hsurf.stratum_retention_interop_tilted_algo.Policy(32)
    assert policy == policy
