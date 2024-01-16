from hsurf.site_selection_strategy.site_selection_algorithms.tilted_eulerian_incidence_rungs_algo import (
    pick_deposition_site,
)

expected8 = [
    4,  # 0
    1,  # 1
    3,  # 2
    2,  # 3
    6,  # 4
    5,  # 5
    0,  # 6
    3,  # 7
    4,  # 8
    1,  # 9
    0,  # 10
    6,  # 11
    4,  # 12
    5,  # 13
    0,  # 14
    4,  # 15
    0,  # 16
    1,  # 17
    0,  # 18
    2,  # 19
    0,  # 20
    5,  # 21
    0,  # 22
    3,  # 23
    0,  # 24
    1,  # 25
    0,  # 26
    6,  # 27
    0,  # 28
    5,  # 29
    0,  # 30
    5,  # 31
    0,  # 32
    1,  # 33
    0,  # 34
    2,  # 35
    0,  # 36
    1,  # 37
    0,  # 38
    3,  # 39
    0,  # 40
    1,  # 41
    0,  # 42
    6,  # 43
    0,  # 44
    1,  # 45
    0,  # 46
    4,  # 47
    0,  # 48
    1,  # 49
    0,  # 50
    2,  # 51
    0,  # 52
    1,  # 53
    0,  # 54
    3,  # 55
    0,  # 56
    1,  # 57
    0,  # 58
    6,  # 59
    0,  # 60
    1,  # 61
    0,  # 62
    6,  # 63
    0,  # 64
    1,  # 65
    0,  # 66
    2,  # 67
    0,  # 68
    1,  # 69
    0,  # 70
    3,  # 71
    0,  # 72
    1,  # 73
    0,  # 74
    2,  # 75
    0,  # 76
    1,  # 77
    0,  # 78
    4,  # 79
    0,  # 80
    1,  # 81
    0,  # 82
    2,  # 83
    0,  # 84
    1,  # 85
    0,  # 86
    3,  # 87
    0,  # 88
    1,  # 89
    0,  # 90
    2,  # 91
    0,  # 92
    1,  # 93
    0,  # 94
    5,  # 95
    0,  # 96
    1,  # 97
    0,  # 98
    2,  # 99
    0,  # 100
    1,  # 101
    0,  # 102
    3,  # 103
    0,  # 104
    1,  # 105
    0,  # 106
    2,  # 107
    0,  # 108
    1,  # 109
    0,  # 110
    4,  # 111
    0,  # 112
    1,  # 113
    0,  # 114
    2,  # 115
    0,  # 116
    1,  # 117
    0,  # 118
    3,  # 119
    0,  # 120
    1,  # 121
    0,  # 122
    2,  # 123
    0,  # 124
    1,  # 125
    0,  # 126
]


def test_pick_deposition_site8():
    surface_size = 8
    for rank in range(len(expected8)):
        assert pick_deposition_site(rank, surface_size) == expected8[rank]


expected16 = [
    8,  # 0
    1,  # 1
    5,  # 2
    2,  # 3
    12,  # 4
    9,  # 5
    4,  # 6
    3,  # 7
    7,  # 8
    6,  # 9
    11,  # 10
    10,  # 11
    14,  # 12
    13,  # 13
    0,  # 14
    4,  # 15
    8,  # 16
    1,  # 17
    5,  # 18
    7,  # 19
    12,  # 20
    9,  # 21
    0,  # 22
    11,  # 23
    8,  # 24
    6,  # 25
    5,  # 26
    14,  # 27
    12,  # 28
    13,  # 29
    0,  # 30
    5,  # 31
]


def test_pick_deposition_site16():
    surface_size = 16
    for rank in range(len(expected16)):
        assert pick_deposition_site(rank, surface_size) == expected16[rank]
