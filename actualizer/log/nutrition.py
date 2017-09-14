import re
from typing import Union

from actualizer import util
from actualizer.log.base import Log
from actualizer.log.base import DATETIME_PATTERN

class NutritionLog(Log):
    MESSAGE_PATTERN = re.compile(r'(?P<VERB>(?:(?:ate)|(?:drank)))', re.IGNORECASE)
    PARSING_PATTERN = re.compile(r'(?P<calories>[0-9]{1,})\s{0,}(?:(?:cal)|(?:cals))\s{1,}(?P<food>.*$)', re.IGNORECASE)
    _FIELDS = ['calories', 'food'] + Log._FIELDS

    def __init__(self, log_request_context: dict) -> 'NutritionLog':
        super().__init__(log_request_context)
        self.nutrition_substr = re.sub(DATETIME_PATTERN, '', self.message).strip()
        self.infer_attributes()

    @property
    def calories(self) -> Union[int, float]:
        return self.__calories

    @calories.setter
    def calories(self, value: Union[str, int, float]) -> None:
        self.__calories = util.convert_numeric(value)

    def infer_attributes(self) -> None:
        matches = self.PARSING_PATTERN.search(self.nutrition_substr)
        if not matches:
            return

        group_dict = matches.groupdict()

        for attr in self._FIELDS:
            if attr in group_dict:
                setattr(self, attr, group_dict[attr])

    def __str__(self) -> str:
        return '{}: {}'.format(self.__class__.__name__, str({x:getattr(self, x) for x in self._FIELDS}))
