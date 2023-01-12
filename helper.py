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


def map_activity_to_dict(activity):
    """Maps activity attributes to a dictionary"""
    temp_dict = {
        'activity_id': activity.__dict__['activity_id'],
        'activity': activity.__dict__['activity'],
        'a_type': activity.__dict__['a_type'],
        'participants': activity.__dict__['participants'],
        'price': activity.__dict__['price'],
        'link': activity.__dict__['link'],
        'accessibility': activity.__dict__['accessibility']
    }
    
    return temp_dict