import pytest
import datetime

from actualizer.log.nutrition import NutritionLog
from actualizer.log.serializers import *

NOW_DT = datetime.datetime.now()

def test_nutrition_parsing():
    log_request = {
            'username': 'jordan',
            'message': 'ate a 100 cal apple 20 min ago',
            'request_time': NOW_DT
            }
    log = NutritionLog(log_request)

    assert log.datetime == NOW_DT - datetime.timedelta(minutes = 20)
    assert log.username == 'jordan'
    assert log.calories == 100
    assert log.nutrition_substr == 'ate a 100 cal apple'
    assert log.food == 'apple'

def test_nutrition_serialization():
    log_request = {
            'username': 'jordan',
            'message': 'ate a 100 cal apple 20 min ago',
            'request_time': NOW_DT
            }
    log = NutritionLog(log_request)
    serialized_dict = log.to_serialized_dict()

    assert serialized_dict['datetime'] == serialize_datetime(NOW_DT - datetime.timedelta(minutes = 20))
    assert serialized_dict['message'] == serialize_message(log_request['message'])
    assert serialized_dict['request_time'] == serialize_request_time(log_request['request_time'])
    assert serialized_dict['food'] == serialize_food('apple')
    assert serialized_dict['calories'] == serialize_calories('100')
    assert serialized_dict['username'] == serialize_username(log_request['username'])
    assert serialized_dict['logtype'] == serialize_logtype('NutritionLog')

def test_nutrition_serialization_with_of_clause():
    log_request = {
            'username': 'jordan',
            'message': 'ate 900 cals of pad kee mao 2 hours ago',
            'request_time': NOW_DT
            }
    log = NutritionLog(log_request)
    serialized_dict = log.to_serialized_dict()

    assert serialized_dict['datetime'] == serialize_datetime(NOW_DT - datetime.timedelta(hours = 2))
    assert serialized_dict['message'] == 'ate 900 cals of pad kee mao 2 hours ago'
    assert serialized_dict['request_time'] == serialize_request_time(log_request['request_time'])
    assert serialized_dict['food'] == 'pad kee mao'
    assert serialized_dict['calories'] == '900'
    assert serialized_dict['username'] == 'jordan'
    assert serialized_dict['logtype'] == 'NutritionLog'

def test_nutrition_serialization_with_today_approx_time():
    log_request = {
            'username': 'special@username',
            'message': 'ate 400 cals of korean appetizers today at noon',
            'request_time': NOW_DT
            }
    log = NutritionLog(log_request)
    serialized_dict = log.to_serialized_dict()

    assert serialized_dict['datetime'] == serialize_datetime(NOW_DT.replace(hour = 12, minute = 0, second = 0, microsecond = 0))
    assert serialized_dict['message'] == 'ate 400 cals of korean appetizers today at noon'
    assert serialized_dict['request_time'] == serialize_request_time(log_request['request_time'])
    assert serialized_dict['food'] == 'korean appetizers'
    assert serialized_dict['calories'] == '400'
    assert serialized_dict['username'] == 'special@username'

def test_nutrition_serialization_with_today_datetime():

    log_request = {
            'username': 'special@username',
            'message': 'ate 600 cals of Korean Beef Tofu Soup today at 12:15',
            'request_time': NOW_DT
            }
    log = NutritionLog(log_request)
    serialized_dict = log.to_serialized_dict()

    assert serialized_dict['datetime'] == serialize_datetime(NOW_DT.replace(hour = 12, minute = 15, second = 0, microsecond = 0))
    assert serialized_dict['message'] == 'ate 600 cals of Korean Beef Tofu Soup today at 12:15'
    assert serialized_dict['request_time'] == serialize_request_time(log_request['request_time'])
    assert serialized_dict['food'] == 'Korean Beef Tofu Soup'
    assert serialized_dict['calories'] == '600'
    assert serialized_dict['username'] == 'special@username'

def test_nutrition_serialization_with_yesterday_datetime():
    log_request = {
            'username': 'jordan',
            'message': 'ate 900 cals of thai food yesterday at 7:00PM',
            'request_time': NOW_DT
            }
    log = NutritionLog(log_request)
    serialized_dict = log.to_serialized_dict()

    assert serialized_dict['datetime'] == serialize_datetime(NOW_DT.replace(minute = 0, second = 0, microsecond = 0, hour = 19) - datetime.timedelta(days = 1))
    assert serialized_dict['message'] == 'ate 900 cals of thai food yesterday at 7:00PM'
    assert serialized_dict['request_time'] == serialize_request_time(log_request['request_time'])
    assert serialized_dict['food'] == 'thai food'
    assert serialized_dict['calories'] == '900'
    assert serialized_dict['username'] == 'jordan'
    assert serialized_dict['logtype'] == 'NutritionLog'

def test_nutrition_serialization_with_yesterday_approxtime():
    log_request = {
            'username': 'jordan',
            'message': 'ate 900 cals of thai food yesterday evening',
            'request_time': NOW_DT,
            }
    log = NutritionLog(log_request)
    serialized_dict = log.to_serialized_dict()

    assert serialized_dict['datetime'] == serialize_datetime(NOW_DT.replace(hour = 18, minute = 0, second = 0, microsecond = 0) - datetime.timedelta(days = 1))
    assert serialized_dict['message'] == 'ate 900 cals of thai food yesterday evening'
    assert serialized_dict['request_time'] == serialize_request_time(log_request['request_time'])
    assert serialized_dict['food'] == 'thai food'
    assert serialized_dict['calories'] == '900'
    assert serialized_dict['username'] == 'jordan'
    assert serialized_dict['logtype'] == 'NutritionLog'

def test_food_regex():
    assert NutritionLog.PARSING_PATTERN

    matches = NutritionLog.PARSING_PATTERN.search('ate 100 cal apple').groupdict()
    assert matches['food'] == 'apple'
    assert matches['calories'] == '100'

    matches = NutritionLog.PARSING_PATTERN.search('ate 10 cal candy bar').groupdict()
    assert matches['food'] == 'candy bar'
    assert matches['calories'] == '10'

    matches = NutritionLog.PARSING_PATTERN.search('ate 0 cal orange').groupdict()
    assert matches['food'] == 'orange'
    assert matches['calories'] == '0'

    matches = NutritionLog.PARSING_PATTERN.search('ate 560 cals of chips').groupdict()
    assert matches['food'] == 'chips'
    assert matches['calories'] == '560'

    matches = NutritionLog.PARSING_PATTERN.search('ate 900 cals of pad kee mao').groupdict()
    assert matches['food'] == 'pad kee mao'
    assert matches['calories'] == '900'

    matches = NutritionLog.PARSING_PATTERN.search('drank 300 calorie latte').groupdict()
    assert matches['food'] == 'latte'
    assert matches['calories'] == '300'

    matches = NutritionLog.PARSING_PATTERN.search('ate 400 cals of korean appetizers').groupdict()
    assert matches['food'] == 'korean appetizers'
    assert matches['calories'] == '400'


