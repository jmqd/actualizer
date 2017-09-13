import re

from actualizer import util
from actualizer.log.base import Log

CALORIES_PATTERN = re.compile(r'(?P<CALORIES_QUANTITY>[0-9]{1,})\s{0,}(?:(?:cal)|(?:cals))')

class NutritionLog(Log):
    MESSAGE_PATTERN = re.compile(r'(?P<VERB>(?:(?:ate)|(?:drank)))')

    def __init__(self, log_request_context: dict) -> 'NutritionLog':
        super().__init__(self, log_request_context)
        self.calories = self.infer_calories()

    def infer_calories(self):
        matches = CALORIES_PATTERN.search(self.message)

        if not matches:
            return None

        return matches.group('CALORIES_QUANTITY')

