import datetime
from actualizer.log import base

def test_relative_datetime_regex():
    matches = base.DATETIME_PATTERN.search('ate a 500 cal sandwich 20 min ago').groupdict()
    assert matches['RELATIVE_DELTA'] == '20 min ago'
    assert matches['TIMEUNIT'] == 'min'
    assert matches['QUANTITY'] == '20'

    matches = base.DATETIME_PATTERN.search('ate 20 samosas 3 hours ago').groupdict()
    assert matches['RELATIVE_DELTA'] == '3 hours ago'
    assert matches['TIMEUNIT'] == 'hours'
    assert matches['QUANTITY'] == '3'

    matches = base.DATETIME_PATTERN.search('ate 20 samosas 3 hrs ago').groupdict()
    assert matches['RELATIVE_DELTA'] == '3 hrs ago'
    assert matches['TIMEUNIT'] == 'hrs'
    assert matches['QUANTITY'] == '3'

    matches = base.DATETIME_PATTERN.search('ate 20 samosas an hour ago').groupdict()
    assert matches['RELATIVE_DELTA'] == 'an hour ago'
    assert matches['TIMEUNIT'] == 'hour'
    assert matches['QUANTITY'] == 'an'

def test_absolute_datetime_regex_with_PM_AM():
    matches = base.DATETIME_PATTERN.search('ate a 100 cal candy bar at 5:00 PM').groupdict()
    assert matches['EXACT_TIME'] == '5:00 PM'

    matches = base.DATETIME_PATTERN.search('ate a 500 cal candy bar at 12:00 PM').groupdict()
    assert matches['EXACT_TIME'] == '12:00 PM'

    matches = base.DATETIME_PATTERN.search('ate a 100 cal candy bar this morning').groupdict()
    assert matches['APPROX_TIME'] == 'morning'

    matches = base.DATETIME_PATTERN.search('ate a 100 cal candy bar at 11').groupdict()
    assert matches['EXACT_TIME'] == '11'

    matches = base.DATETIME_PATTERN.search('ate a 12300 cal candy bar at 5P').groupdict()
    assert matches['EXACT_TIME'] == '5P'

    matches = base.DATETIME_PATTERN.search('ate a 12300 cal candy bar at 1A').groupdict()
    assert matches['EXACT_TIME'] == '1A'

    matches = base.DATETIME_PATTERN.search('ate a 12300 cal candy bar at 1:00AM').groupdict()
    assert matches['EXACT_TIME'] == '1:00AM'

    matches = base.DATETIME_PATTERN.search('ate a 12300 cal candy bar at 3:00P').groupdict()
    assert matches['EXACT_TIME'] == '3:00P'

def test_exact_datetime_regex_with_modifier():
    matches = base.DATETIME_PATTERN.search('ate a 300 cal donut yesterday at 2:00PM').groupdict()
    assert matches['EXACT_TIME'] == '2:00PM'
    assert matches['MODIFIER'] == 'yesterday'

    matches = base.DATETIME_PATTERN.search('ate a 300 cal donut today at 2:00PM').groupdict()
    assert matches['EXACT_TIME'] == '2:00PM'

    matches = base.DATETIME_PATTERN.search('ate a 300 cal donut today at 2').groupdict()
    assert matches['EXACT_TIME'] == '2'

def test_approx_datetime_regex_with_yesterday():
    matches = base.DATETIME_PATTERN.search('ate a 300 cal donut yesterday morning').groupdict()
    assert matches['APPROX_TIME'] == 'morning'
    assert matches['MODIFIER'] == 'yesterday'

def test_infer_datetime():
    log_request = {
            'request_time': base.NOW_DT,
            'username': 'jordan',
            'message': 'ate 300 cal latte 20 min ago'
            }
    log = base.Log(log_request)
    assert log.datetime == base.NOW_DT - datetime.timedelta(minutes = 20)

    dt = datetime.datetime(2016, 11, 30, 10, 22, 21)
    log_request = {
            'request_time': dt,
            'username': 'jordan',
            'message': 'ate 300 cal latte 4 hours ago'
            }
    log = base.Log(log_request)
    assert log.datetime == dt - datetime.timedelta(hours = 4)

