from functools import lru_cache
@lru_cache(None)
def win_a_dollar(red, black):
    if red == 0:
        return 0
    if black == 0:
        return red
    return max(red/(red+black)*(1 + win_a_dollar(red-1, black)) + \
        black/(red+black) * (-1 + win_a_dollar(red, black-1)), 0)
print(win_a_dollar(200, 200))