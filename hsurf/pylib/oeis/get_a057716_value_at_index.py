# https://oeis.org/A057716
def get_a057716_value_at_index(n: int) -> int:
    return n + (n + (n).bit_length()).bit_length()
