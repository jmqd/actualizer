from typing import Union
from decimal import *

class Potential:
    pass

class IntervalAggregateBooundedPotential(Potential):
    def __init__(self, interval: str, interval_qty: int, aggregation_field: str,
                 aggregator: callable, constant_bound: Union[int, float, Decimal],
                 bound_cmp: callable) -> Potential:
        pass

class NutritionPotential(Potential):
    def __init__(self, interval: str,

