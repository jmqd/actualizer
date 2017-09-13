from actualizer.log import client
from actualizer.log import nutrition

def test_LOG_SUBCLASSES():
    assert client.LOG_SUBCLASSES == [nutrition.NutritionLog]

def test_get_log_type():
    nutrition_message = 'ate 500 cal muffin'
    assert client.get_log_type(nutrition_message) == nutrition.NutritionLog
