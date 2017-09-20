from typing import List
from typing import Union
from typing import Optional
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
        'secs': 'seconds',
        'yesterday': 'days',
        'today': 'days',
        'this': 'days'
        }

DEFAULT_QTY_FOR_INTERVAL = {
        'today': 0,
        'yesterday': 1,
        'this': 0
        }

FUZZY_DATETIME_MAPPING = {
        'noon': lambda x: x.replace(hour = 12, minute = 0, second = 0, microsecond = 0),
        'evening': lambda x: x.replace(hour = 18, minute = 0, second = 0, microsecond = 0),
        'afternoon': lambda x: x.replace(hour = 14, minute = 0, second = 0, microsecond = 0),
        'morning': lambda x: x.replace(hour = 9, minute = 0, second = 0, microsecond = 0),
        }

def get_all_subclasses(cls: type) -> List[type]:
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses

def get_timedelta(qty: Optional[Union[int, float]], interval: str) -> datetime.timedelta:
    interval_kwarg = TIMEUNIT_MAP[interval]
    interval_qty = convert_numeric(qty) if qty is not None else DEFAULT_QTY_FOR_INTERVAL[interval]
    return datetime.timedelta(**{interval_kwarg: interval_qty})

def convert_numeric(num_str: str) -> Union[int, float]:
    try:
        return float(num_str)
    except:
        return int(num_str)

def convert_to_int(num: Union[str, int, float]) -> int:
    return int(convert_numeric(num))

def convert_approx_time_to_dt(fuzzy_datetime: str) -> datetime.datetime:
    now = datetime.datetime.now()

    if fuzzy_datetime.lower() in FUZZY_DATETIME_MAPPING:
        return FUZZY_DATETIME_MAPPING.get(fuzzy_datetime.lower())(now)

def get_datetime_from_timestr(hour: int, minute: int, mode: str=None) -> datetime.datetime:
    now = datetime.datetime.now()
    now = now.replace(minute = 0, second = 0, microsecond = 0, hour = 0)

    if not mode:
        pass
    elif mode.lower() in ('am', 'a') and hour == 12:
        hour = 0
    elif mode.lower() in ('pm', 'p') and hour < 12:
        hour = hour + 12

    return now.replace(hour = hour, minute = minute)

