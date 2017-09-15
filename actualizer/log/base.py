import re
import datetime
from actualizer import util

TIMEUNIT_PATTERN = r'(?P<TIMEUNIT>{})'.format('|'.join(['(?:{})'.format(k) for k in util.TIMEUNIT_MAP]))
TOKENS_PRECEEDING_TIMEUNIT = r'(?P<QUANTITY>(?:[0-9]{1,})|(?:a few)|(?:an))'
TOKENS_SUCCEEDING_TIMEUNIT = r'(?P<RELATIVE_DIRECTION>(?:ago)|(?:earlier))'
FIXED_RELATIVE_TOKENS = r'(?P<FIXED_RELATIVE>(?:yesterday)|(?:today))'
RELATIVE_DELTA_PATTERN = r'(?P<RELATIVE_DELTA>' + '|'.join([r'\s{1,}'.join([TOKENS_PRECEEDING_TIMEUNIT, TIMEUNIT_PATTERN, TOKENS_SUCCEEDING_TIMEUNIT]), FIXED_RELATIVE_TOKENS]) + r')'
ABSOLUTE_DATETIME_PATTERN = r'(?:(?:at)|(?:this))\s{1,}(?P<ABSOLUTE_TIME>(?:(?:noon)|(?:midnight)|(?:morning)|(?:afternoon)|(?:evening))|(?:(?:\d{1,2})(?::\d{2})?(?:\s?(?:PM?)|(?:AM?))?))'
DATETIME_PATTERN = re.compile('|'.join([RELATIVE_DELTA_PATTERN, ABSOLUTE_DATETIME_PATTERN]), re.IGNORECASE)
NOW_DT = datetime.datetime.now()

# TODO
# - finish infer_datetime implementation
#
# Implement:
#   - NutritionLog
#   - ExerciseLog
#   - TaskLog
#   - SleepLog (?)



class Log:
    _FIELDS = ['username', 'message', 'request_time', 'datetime']
    FIELD_SERIALIZER = {
            'username': str,
            'message': str,
            'request_time': lambda x: x.isoformat(),
            'datetime': lambda x: x.isoformat()
            }

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

        if 'ABSOLUTE_TIME' in groupdict:
            return util.convert_fuzzy_time_to_dt(groupdict['ABSOLUTE_TIME'])

    def to_serialized_dict(self) -> dict:
        return {k: self.FIELD_SERIALIZER[k](getattr(self, k)) for k in self._FIELDS}

