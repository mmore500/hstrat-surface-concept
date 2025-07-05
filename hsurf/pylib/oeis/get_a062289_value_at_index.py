from .get_a057716_value_at_index import get_a057716_value_at_index


# https://oeis.org/A062289
def get_a062289_value_at_index(n: int) -> int:
    return get_a057716_value_at_index(n + 1) - 1
