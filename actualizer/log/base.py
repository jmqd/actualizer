import re
import datetime

TIMEUNIT_PATTERN = r'(?P<TIMEUNIT>(?:min)|(?:minute)|(?:minutes)|(?:seconds)|(?:secs)|(?:m)|(?:s)|(?:hrs)|(?:hours)|(?:hr)|(?:h)|(?:d)|(?:days))'
TOKENS_PRECEEDING_TIMEUNIT = r'(?P<QUANTITY>(?:[0-9]{1,})|(?:a few))'
TOKENS_SUCCEEDING_TIMEUNIT = r'(?P<RELATIVE_DIRECTION>(?:ago)|(?:earlier))'
FIXED_RELATIVE_TOKENS = r'(?P<FIXED_RELATIVE>(?:yesterday)|(?:today))'
RELATIVE_DELTA_PATTERN = r'(?P<RELATIVE_DELTA>' + '|'.join([r'\s{1,}'.join([TOKENS_PRECEEDING_TIMEUNIT, TIMEUNIT_PATTERN, TOKENS_SUCCEEDING_TIMEUNIT]), FIXED_RELATIVE_TOKENS]) + r')'
ABSOLUTE_DATETIME_PATTERN = r'(?P<ABSOLUTE>(?:at (?:(?:noon)|(?:[0-9]{1,2})|(?:midnight)))|(?:this (?:(?:morning)|(?:afternoon)|(?:evening))))'
DATETIME_PATTERN = re.compile('|'.join([RELATIVE_DELTA_PATTERN, ABSOLUTE_DATETIME_PATTERN]))

# TODO
# - finish infer_datetime implementation
#
# Implement:
#   - NutritionLog
#   - ExerciseLog
#   - TaskLog
#   - SleepLog (?)

class Log:
    DATETIME_PATTERN = re.compile(DATETIME_PATTERN)

    def __init__(self, log_request_context: dict) -> 'Log':
        self.username = log_request_context['username']
        self.message = log_request_context['message']
        self.datetime = self.infer_datetime()

    def infer_datetime(self) -> datetime.datetime:
        matches = DATETIME_PATTERN.search(self.message)


class NutritionLog(Log):
    def __init__(self, log_request_context: dict) -> 'NutritionLog':
        super().__init__(self, log_request_context)
        self.calories = self.infer_calories()

