import datetime
from decimal import *
from operator import __lt__
from actualizer.potential import AggregatedIntervalBoundedPotential

def test_interval_aggregate_bounded_potential():
    potential_db_item = {'aggregator': 'sum',
                         'field': 'calories',
                         'potential': 2000,
                         'comparator': '__lt__',
                         'timedelta_interval': 'day',
                         'timedelta_interval_qty': 1
                         }
    bounded_potential = AggregatedIntervalBoundedPotential(**potential_db_item)

    assert bounded_potential.aggregator == 'sum'
    assert bounded_potential.field == 'calories'
    assert bounded_potential.potential == 2000
    assert bounded_potential.comparator == '__lt__'
    assert bounded_potential.timedelta_interval == 'day'
    assert bounded_potential.timedelta_interval_qty == 1

    # testing some of the protected members
    _comparator = bounded_potential.__dict__['_comparator']
    _aggregator = bounded_potential.__dict__['_aggregator']
    _timedelta = bounded_potential.__dict__['_timedelta']

    assert _comparator == __lt__
    assert _aggregator == sum
    assert _timedelta == datetime.timedelta(days = 1)

    data_fat_day = [
	{'username': 'jordan', 'food': 'pizza', 'datetime': '2017-09-15T12:52:13.647062', 'calories': Decimal('700'), 'request_time': '2017-09-15T02:52:13.619742', 'logtype': 'NutritionLog', 'message': 'ate 700 cal of pizza at noon'},
        {'username': 'jordan', 'food': 'falafel', 'datetime': '2017-09-15T16:57:52.470204', 'calories': Decimal('650'), 'request_time': '2017-09-15T02:57:52.470204', 'logtype': 'NutritionLog', 'message': 'ate 650 cal of falafel 10 hours ago'},
        {'username': 'jordan', 'food': 'hot chocolate', 'datetime': '2017-09-15T19:54:51.849280', 'calories': Decimal('200'), 'request_time': '2017-09-15T02:54:51.849280', 'logtype': 'NutritionLog', 'message': 'ate 200 cal hot chocolate 7 hours ago'},
        {'username': 'jordan', 'food': 'meat balls', 'datetime': '2017-09-15T21:55:48.604270', 'calories': Decimal('500'), 'request_time': '2017-09-15T02:55:48.604270', 'logtype': 'NutritionLog', 'message': 'ate 500 cal of meat balls 5 hours ago'},
        {'username': 'jordan', 'food': 'salt water taffy', 'datetime': '2017-09-15T21:56:53.345039', 'calories': Decimal('200'), 'request_time': '2017-09-15T02:56:53.345039', 'logtype': 'NutritionLog', 'message': 'ate 200 cal of salt water taffy 5 hours ago'},
        {'username': 'jordan', 'food': 'cider', 'datetime': '2017-09-15T22:57:06.018790', 'calories': Decimal('100'), 'request_time': '2017-09-15T02:57:06.018790', 'logtype': 'NutritionLog', 'message': 'ate 100 cal of cider 4 hours ago'},
        {'username': 'jordan', 'food': 'beef', 'datetime': '2017-09-15T11:50:08.387163', 'calories': Decimal('500'), 'request_time': '2017-09-17T00:50:08.387163', 'logtype': 'NutritionLog', 'message': 'ate 500 cal of beef 13 hours ago'},
        {'username': 'jordan', 'food': 'coca cola', 'datetime': '2017-09-15T12:50:54.663966', 'calories': Decimal('250'), 'request_time': '2017-09-17T00:50:54.663966', 'logtype': 'NutritionLog', 'message': 'ate 250 cal of coca cola 12 hours ago'},
        {'username': 'jordan', 'food': 'chinese bbq', 'datetime': '2017-09-15T14:51:29.810521', 'calories': Decimal('800'), 'request_time': '2017-09-17T00:51:29.810521', 'logtype': 'NutritionLog', 'message': 'ate 800 cal of chinese bbq 10 hours ago'},
        {'username': 'jordan', 'food': 'cookies', 'datetime': '2017-09-15T18:51:47.406069', 'calories': Decimal('200'), 'request_time': '2017-09-17T00:51:47.406069', 'logtype': 'NutritionLog', 'message': 'ate 200 cal of cookies 6 hours ago'}
        ]

    assert bounded_potential.get_actual(data_fat_day) == 4100
    assert bounded_potential.is_actualized(data_fat_day) == False
    assert bounded_potential.get_actualization_distance(data_fat_day) == 2100

