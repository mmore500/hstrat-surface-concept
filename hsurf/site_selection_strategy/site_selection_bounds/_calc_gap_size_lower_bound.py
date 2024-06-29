def calc_gap_size_lower_bound(rank: int, surface_size: int) -> int:
    naive = rank // surface_size
    res = (max(rank + 1 - surface_size, 0) + surface_size) // (surface_size + 1)
    # res = (max(rank + 1 - surface_size, 0) + surface_size) // (surface_size + 1)
    # aka
    res = (rank + 1) // (surface_size + 1)
    assert res <= naive
    return res
