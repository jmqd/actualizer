from operator import __lt__
from typing import Union
from typing import List
from decimal import *
from actualizer import util

class Potential: pass

class AggregatedIntervalBoundedPotential(Potential):
    def __init__(self, timedelta_interval: str, timedelta_interval_qty: int,
                 field: str, aggregator: str, potential: Union[int, float, Decimal],
                 comparator: str) -> Potential:
        # deserializable (inherent descriptive) properties
        self.timedelta_interval = timedelta_interval
        self.timedelta_interval_qty = timedelta_interval_qty
        self.field = field
        self.aggregator = aggregator
        self.potential = potential
        self.comparator = comparator

        # derived properties
        self._timedelta = util.get_timedelta(timedelta_interval_qty, timedelta_interval)
        self._aggregator = eval(aggregator)
        self._comparator = eval(comparator)

    def get_actualization_distance(self, data: List[dict]) -> int:
        actual = self.get_actual(data)
        return abs(actual - self.potential)

    def get_actual(self, data: List[dict]) -> bool:
        '''Assumes data is all in a single period interval.'''
        actual = self._aggregator([x.get(self.field) for x in data])
        return actual

    def is_actualized(self, data: List[dict]) -> bool:
        '''Given a list of data, see if it complies with the bound.
        Note:
            For now, ignoring the interval logic. Assuming that caller correctly
            provides only a day's worth of data
        '''
        actual = self._aggregator([x.get(self.field) for x in data])
        return self._comparator(actual, self.potential)

class NutritionPotential(AggregatedIntervalBoundedPotential): pass

