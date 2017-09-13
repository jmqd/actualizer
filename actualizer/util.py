from typing import List, Union
import datetime

TIMEUNIT_MAP = {
        'd': 'days',
        'day': 'days',
        'days': 'days',
        'h': 'hours',
        'hr': 'hours',
        'hours': 'hours',
        'hrs': 'hours',
        'hour': 'hours',
        'm': 'minutes',
        'min': 'minutes',
        'mins': 'minutes',
        's': 'seconds',
        'sec': 'seconds',
        'secs': 'seconds'
        }

def get_all_subclasses(cls: type) -> List[type]:
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses

def get_timedelta(qty: Union[int, float], interval: str) -> datetime.timedelta:
    return datetime.timedelta(**{TIMEUNIT_MAP[interval]: convert_numeric(qty)})

def convert_numeric(num_str: str) -> Union[int, float]:
    try:
        return float(num_str)
    except:
        return int(num_str)

