from typing import List

def get_all_subclasses(cls: type) -> List[type]:
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses

def convert_estimate_to_timedelta(estimate_str: str) -> datetime.timedelta:
    '''Takes the user input string for time deltas and converts it to a `datetime.timedelta`
    e.g.
        - 4h30m   -> datetime.timedelta(hours = 4, minutes = 30)
        - 3d2h10m -> datetime.timedelta(days = 3, hours = 2, minutes = 10)
        - 2.5d1h  -> datetime.timedelta(days = 2, hours = 13)
    Note:
        I've made the recursive implementation a closure so as to not pollute
        the calling signature.
    '''
    def convert_recursive_impl(estimate_str: str, td: datetime.timedelta) -> datetime.timedelta:
        if not estimate_str:
            return td

        for i, char in enumerate(estimate_str):
            if char.isalpha():
                qty = convert_numeric(estimate_str[:i])
                return convert_recursive_impl(estimate_str[i + 1:], get_timedelta(qty, char) + td)

    return convert_recursive_impl(estimate_str, datetime.timedelta())

def get_timedelta(qty: Union[int, float], interval: str) -> datetime.timedelta:
    return datetime.timedelta(**{interval_map[interval]: qty})

def convert_numeric(num_str: str) -> Union[int, float]:
    try:
        return float(num_str)
    except:
        return int(num_str)

