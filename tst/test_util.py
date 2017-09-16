import pytest
import datetime
from actualizer import util

def test_get_all_subclasses():
    class Foo: pass
    class Bar(Foo): pass
    class FooBar(Bar): pass

    assert util.get_all_subclasses(Foo) == [Bar, FooBar]
    assert util.get_all_subclasses(Bar) == [FooBar]
    assert util.get_all_subclasses(FooBar) == []

def test_convert_numeric():
    assert util.convert_numeric('2') == 2
    assert util.convert_numeric('1') == 1
    assert util.convert_numeric('0') == 0
    assert util.convert_numeric('0.5') == 0.5
    assert util.convert_numeric('2.5') == 2.5

def test_get_timedelta():
    assert util.get_timedelta(5, 'd') == datetime.timedelta(days = 5)
    assert util.get_timedelta(10, 'day') == datetime.timedelta(days = 10)
    assert util.get_timedelta(51, 'days') == datetime.timedelta(days = 51)
    assert util.get_timedelta(50, 's') == datetime.timedelta(seconds = 50)
    assert util.get_timedelta(50, 'sec') == datetime.timedelta(seconds = 50)
    assert util.get_timedelta(50, 'secs') == datetime.timedelta(seconds = 50)
    assert util.get_timedelta(1, 'h') == datetime.timedelta(hours = 1)
    assert util.get_timedelta(2.4, 'hr') == datetime.timedelta(hours = 2.4)
    assert util.get_timedelta(1.4, 'hrs') == datetime.timedelta(hours = 1.4)
    assert util.get_timedelta(3, 'hours') == datetime.timedelta(hours = 3)
    assert util.get_timedelta(20, 'm') == datetime.timedelta(minutes = 20)
    assert util.get_timedelta(2.5, 'min') == datetime.timedelta(minutes = 2.5)
    assert util.get_timedelta(10, 'mins') == datetime.timedelta(minutes = 10)

def test_convert_approx_time_to_dt():
    noon = truncate_datetime_to_hour_precision(datetime.datetime.now().replace(hour = 12))
    evening = truncate_datetime_to_hour_precision(datetime.datetime.now().replace(hour = 18))
    afternoon = truncate_datetime_to_hour_precision(datetime.datetime.now().replace(hour = 14))
    morning = truncate_datetime_to_hour_precision(datetime.datetime.now().replace(hour = 9))

    assert truncate_datetime_to_hour_precision(util.convert_approx_time_to_dt('noon')) == noon
    assert truncate_datetime_to_hour_precision(util.convert_approx_time_to_dt('evening')) == evening
    assert truncate_datetime_to_hour_precision(util.convert_approx_time_to_dt('afternoon')) == afternoon
    assert truncate_datetime_to_hour_precision(util.convert_approx_time_to_dt('morning')) == morning

def truncate_datetime_to_hour_precision(dt: datetime.datetime) -> datetime.datetime:
    return dt.replace(minute = 0, second = 0, microsecond = 0)

def test_convert_to_int():
    assert util.convert_to_int('5') == 5
    assert util.convert_to_int('-1') == -1
    assert util.convert_to_int('-0.5') == 0
    assert util.convert_to_int('2.5') == 2
    assert util.convert_to_int('123.32') == 123
    assert util.convert_to_int('123.99') == 123
    assert util.convert_to_int('1412') == 1412
    assert util.convert_to_int('0.00000001') == 0
    assert util.convert_to_int('31.3451') == 31
    assert util.convert_to_int('0') == 0
    assert util.convert_to_int('0.7') == 0
