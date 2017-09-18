import pytest
import datetime
from actualizer.util import *

def test_get_all_subclasses():
    class Foo: pass
    class Bar(Foo): pass
    class FooBar(Bar): pass

    assert get_all_subclasses(Foo) == [Bar, FooBar]
    assert get_all_subclasses(Bar) == [FooBar]
    assert get_all_subclasses(FooBar) == []

def test_convert_numeric():
    assert convert_numeric('2') == 2
    assert convert_numeric('1') == 1
    assert convert_numeric('0') == 0
    assert convert_numeric('0.5') == 0.5
    assert convert_numeric('2.5') == 2.5

def test_get_timedelta():
    assert get_timedelta(5, 'd') == datetime.timedelta(days = 5)
    assert get_timedelta(10, 'day') == datetime.timedelta(days = 10)
    assert get_timedelta(51, 'days') == datetime.timedelta(days = 51)
    assert get_timedelta(50, 's') == datetime.timedelta(seconds = 50)
    assert get_timedelta(50, 'sec') == datetime.timedelta(seconds = 50)
    assert get_timedelta(50, 'secs') == datetime.timedelta(seconds = 50)
    assert get_timedelta(1, 'h') == datetime.timedelta(hours = 1)
    assert get_timedelta(2.4, 'hr') == datetime.timedelta(hours = 2.4)
    assert get_timedelta(1.4, 'hrs') == datetime.timedelta(hours = 1.4)
    assert get_timedelta(3, 'hours') == datetime.timedelta(hours = 3)
    assert get_timedelta(20, 'm') == datetime.timedelta(minutes = 20)
    assert get_timedelta(2.5, 'min') == datetime.timedelta(minutes = 2.5)
    assert get_timedelta(10, 'mins') == datetime.timedelta(minutes = 10)
    assert get_timedelta(None, 'yesterday') == datetime.timedelta(days = 1)
    assert get_timedelta(None, 'today') == datetime.timedelta(days = 0)

def test_convert_approx_time_to_dt():
    # TODO: I think this function is wrong. (test and util impl)
    noon = truncate_datetime_to_hour_precision(datetime.datetime.now().replace(hour = 12))
    evening = truncate_datetime_to_hour_precision(datetime.datetime.now().replace(hour = 18))
    afternoon = truncate_datetime_to_hour_precision(datetime.datetime.now().replace(hour = 14))
    morning = truncate_datetime_to_hour_precision(datetime.datetime.now().replace(hour = 9))

    assert truncate_datetime_to_hour_precision(convert_approx_time_to_dt('noon')) == noon
    assert truncate_datetime_to_hour_precision(convert_approx_time_to_dt('evening')) == evening
    assert truncate_datetime_to_hour_precision(convert_approx_time_to_dt('afternoon')) == afternoon
    assert truncate_datetime_to_hour_precision(convert_approx_time_to_dt('morning')) == morning

def truncate_datetime_to_hour_precision(dt: datetime.datetime) -> datetime.datetime:
    return dt.replace(minute = 0, second = 0, microsecond = 0)

def test_convert_to_int():
    assert convert_to_int('5') == 5
    assert convert_to_int('-1') == -1
    assert convert_to_int('-0.5') == 0
    assert convert_to_int('2.5') == 2
    assert convert_to_int('123.32') == 123
    assert convert_to_int('123.99') == 123
    assert convert_to_int('1412') == 1412
    assert convert_to_int('0.00000001') == 0
    assert convert_to_int('31.3451') == 31
    assert convert_to_int('0') == 0
    assert convert_to_int('0.7') == 0

def test_get_datetime_from_timestr_12_AM():
    today = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    assert get_datetime_from_timestr(12, 0, 'AM') == today + datetime.timedelta(hours = 0)

def test_get_datetime_from_timestr_1230_PM():
    today = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    assert get_datetime_from_timestr(12, 30, 'PM') == today + datetime.timedelta(hours = 12, minutes = 30)

def test_get_datetime_from_timestr_559_PM():
    today = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    assert get_datetime_from_timestr(5, 59, 'PM') == today + datetime.timedelta(hours = 17, minutes = 59)

def test_get_datetime_from_timestr_17():
    today = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    assert get_datetime_from_timestr(17, 0) == today + datetime.timedelta(hours = 17)

def test_get_datetime_from_timestr_4_PM():
    today = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    assert get_datetime_from_timestr(4, 0, 'PM') == today + datetime.timedelta(hours = 16)

def test_get_datetime_from_timestr_9_P():
    today = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    assert get_datetime_from_timestr(9, 0, 'P') == today + datetime.timedelta(hours = 21)

def test_get_datetime_from_timestr_5_AM():
    today = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    assert get_datetime_from_timestr(5, 0, 'AM') == today + datetime.timedelta(hours = 5)

def test_get_datetime_from_timestr_2_A():
    today = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    assert get_datetime_from_timestr(2, 0, 'A') == today + datetime.timedelta(hours = 2)

