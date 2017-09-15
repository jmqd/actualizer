import datetime
from unittest import mock
from mock import patch
from actualizer.log.serializers import *
from actualizer import util

def test_serialize_calories():
    with patch('actualizer.util.convert_to_int') as convert_to_int_mocked:
        serialize_calories('500')
        convert_to_int_mocked.assert_called_with('500')

        serialize_calories(121)
        convert_to_int_mocked.assert_called_with(121)

        serialize_calories('501.1')
        convert_to_int_mocked.assert_called_with('501.1')

    assert serialize_calories(10) == 10
    assert serialize_calories('10') == 10
    assert serialize_calories(10.5) == 10
    assert serialize_calories(0) == 0
    assert serialize_calories('0') == 0
    assert serialize_calories('213') == 213

def test_serialize_username():
    assert serialize_username('foo') == 'foo'
    assert serialize_username('') == ''

    a = []
    assert serialize_username(a) == a

