from ..get_powersof2triangle_val_at_index import get_powersof2triangle_val_at_index

from .get_longevity_level_of_index import get_longevity_level_of_index
from .get_longevity_offset_of_level import get_longevity_offset_of_level


def get_longevity_ordered_position_of_index(index: int, num_indices: int) -> int:
    longevity_level = get_longevity_level_of_index(index)
    position_within_level = (
        get_powersof2triangle_val_at_index(index - 1) if index else 0
    )

    offset = get_longevity_offset_of_level(longevity_level, num_indices)
    spacing = offset * 2
    return offset + spacing * position_within_level
