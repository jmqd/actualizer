import pytest
import datetime

from actualizer.log.nutrition import NutritionLog

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
