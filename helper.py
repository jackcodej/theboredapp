"""Helper functions to reduce duplicate code in server.py"""

def convert_arg_to_percent(range_str):
    """Converts range string to float"""

    if range_str != '':
        range_str = int(range_str)/100

    return range_str


def check_range_values(min, max):
    """Swaps min and max if min is greater than max"""

    if min > max:
        temp = min
        min = max
        max = temp

    return min, max
