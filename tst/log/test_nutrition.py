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

