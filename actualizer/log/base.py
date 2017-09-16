import re
import datetime
from actualizer import util
from actualizer.log.serializers import *

# Holy shit this is a mess.
TIMEUNIT_PATTERN = r'(?P<TIMEUNIT>{})'.format('|'.join(['(?:{})'.format(k) for k in util.TIMEUNIT_MAP]))
TOKENS_PRECEEDING_TIMEUNIT = r'(?P<QUANTITY>(?:[0-9]{1,})|(?:a few)|(?:an))'
TOKENS_SUCCEEDING_TIMEUNIT = r'(?P<RELATIVE_DIRECTION>(?:ago)|(?:earlier))'
FIXED_RELATIVE_TOKENS = r'(?P<FIXED_RELATIVE>(?:yesterday)|(?:today))'
RELATIVE_DELTA_PATTERN = r'(?P<RELATIVE_DELTA>' + '|'.join([r'\s{1,}'.join([TOKENS_PRECEEDING_TIMEUNIT, TIMEUNIT_PATTERN, TOKENS_SUCCEEDING_TIMEUNIT]), FIXED_RELATIVE_TOKENS]) + r')'
APPROXIMATE_TIMES = r'(?P<APPROX_TIME>(?:(?:noon)|(?:midnight)|(?:morning)|(?:afternoon)|(?:evening)))'
EXACT_TIMES = r'(?P<EXACT_TIME>(?P<hour>\d{1,2})(?P<minute>\:\d{2})?(?P<mode>(?:\s)?(?:(?:PM?)|(?:AM?)))?)'
TOKENS_PRECEEDING_TIMES = r'(?:(?:at)|(?:this))'
ABSOLUTE_DATETIME_PATTERN = r'(?P<ABSOLUTE>' + TOKENS_PRECEEDING_TIMES + r'\s{1,}' + r'(?:' + '|'.join([APPROXIMATE_TIMES, EXACT_TIMES]) + r'))'
DATETIME_PATTERN = re.compile('|'.join([RELATIVE_DELTA_PATTERN, ABSOLUTE_DATETIME_PATTERN]), re.IGNORECASE)
print(DATETIME_PATTERN.pattern)
NOW_DT = datetime.datetime.now()

# TODO
#   - ExerciseLog
#   - TaskLog
#   - SleepLog (?)

class Log:

    FIELDS = ['username', 'message', 'request_time', 'datetime']
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
            return self.request_time - util.get_timedelta(groupdict['QUANTITY'], groupdict['TIMEUNIT'])

        if 'APPROX_TIME' in groupdict:
            return util.convert_approx_time_to_dt(groupdict['APPROX_TIME'])

        if 'EXACT_TIME' in groupdict:
            hour = int(groupdict.get('hour'))
            minute = int(groupdict.get('minute', 0))
            return util.get_datetime_from_timestr(hour, minute)

    def to_serialized_dict(self) -> dict:
        return {k: self.FIELD_SERIALIZER[k](getattr(self, k)) for k in self.FIELDS}

