import re
import datetime
from actualizer import util
from actualizer.log.serializers import *

# Holy shit this is a mess.
TIMEUNIT_PATTERN = r'(?P<TIMEUNIT>{})'.format('|'.join(['(?:{})'.format(k) for k in util.TIMEUNIT_MAP]))
TOKENS_PRECEEDING_TIMEUNIT = r'(?P<QUANTITY>(?:[0-9]{1,})|(?:a few)|(?:an))'
TOKENS_SUCCEEDING_TIMEUNIT = r'(?P<RELATIVE_DIRECTION>(?:ago)|(?:earlier))'
APPROXIMATE_TIMES = r'(?P<APPROX_TIME>(?:(?:noon)|(?:midnight)|(?:morning)|(?:afternoon)|(?:evening)))'
EXACT_TIMES = r'(?P<EXACT_TIME>(?P<hour>\d{1,2})(?:\:(?P<minute>\d{2}))?(?P<mode>(?:\s)?(?:(?:PM?)|(?:AM?)))?)'
TOKENS_PRECEEDING_TIMES = r'(?:(?P<MODIFIER>(?:yesterday)|(?:today))\s{1,})?(?:(?:at)|(?:this))'
TOKENS_PRECEEDING_APPROX_TIMES = r'(?P<APPROX_MODIFIER>(?:yesterday)|(?:today)|(?:this))'

APPROX_TIMES = r'\s{1,}'.join([TOKENS_PRECEEDING_APPROX_TIMES, APPROXIMATE_TIMES])
RELATIVE_DELTA_PATTERN = r'(?P<RELATIVE_DELTA>' + r'\s{1,}'.join([TOKENS_PRECEEDING_TIMEUNIT, TIMEUNIT_PATTERN, TOKENS_SUCCEEDING_TIMEUNIT])  + r')'
ABSOLUTE_DATETIME_PATTERN = r'(?P<ABSOLUTE>' + TOKENS_PRECEEDING_TIMES + r'\s{1,}' + r'(?:' + EXACT_TIMES + r'))'
APPROX_DATETIME_PATTERN = TOKENS_PRECEEDING_APPROX_TIMES + r'\s{1,}' + APPROXIMATE_TIMES
DATETIME_PATTERN = re.compile('|'.join([RELATIVE_DELTA_PATTERN, ABSOLUTE_DATETIME_PATTERN, APPROX_DATETIME_PATTERN]), re.IGNORECASE)
NOW_DT = datetime.datetime.now()

# TODO
#   - ExerciseLog
#   - TaskLog
#   - SleepLog (?)

class Log:

    FIELDS = ['username', 'message', 'request_time', 'datetime', 'logtype']
    FIELD_SERIALIZER = {k:eval('serialize_{}'.format(k)) for k in FIELDS}

    def __init__(self, log_request_context: dict) -> 'Log':
        self.username = log_request_context['username']
        self.message = log_request_context['message']
        self.request_time = log_request_context['request_time']
        self.datetime = self.infer_datetime()

    def infer_datetime(self) -> datetime.datetime:
        matches = DATETIME_PATTERN.search(self.message)

        if not matches:
            return None

        groupdict = {k:v for k, v in matches.groupdict().items() if v is not None}

        if 'RELATIVE_DELTA' in groupdict:
            datetime = self.request_time - util.get_timedelta(groupdict['QUANTITY'], groupdict['TIMEUNIT'])

        if 'APPROX_TIME' in groupdict:
            datetime = util.convert_approx_time_to_dt(groupdict['APPROX_TIME'])

        if 'EXACT_TIME' in groupdict:
            hour = int(groupdict.get('hour'))
            minute = int(groupdict.get('minute', 0))
            datetime = util.get_datetime_from_timestr(hour, minute)

        if 'MODIFIER' in groupdict:
            datetime - util.get_timedelta(interval = groupdict['MODIFIER'])

        return datetime


    @property
    def logtype(self):
        return self.__class__.__name__

    def to_serialized_dict(self) -> dict:
        return {k: self.FIELD_SERIALIZER[k](getattr(self, k)) for k in self.FIELDS}

