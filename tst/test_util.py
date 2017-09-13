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


