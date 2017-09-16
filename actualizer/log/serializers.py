import datetime
from typing import Union
from actualizer import util

def serialize_username(username: str) -> str:
    return username

def serialize_message(message: str) -> str:
    return message

def serialize_request_time(request_time: datetime.datetime) -> str:
    return request_time.isoformat()

def serialize_datetime(_datetime: datetime.datetime) -> str:
    return _datetime.isoformat()

def serialize_calories(calories: Union[int, float, str]) -> int:
    return str(util.convert_to_int(calories))

def serialize_food(food: str) -> str:
    return str(food)

def serialize_logtype(logtype: str) -> str:
    return logtype

