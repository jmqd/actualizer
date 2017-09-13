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

