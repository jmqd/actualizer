from actualizer.api.request import ListLogsRequestContext
from actualizer.dao import LogTableDao
import datetime

NOW_DT = datetime.datetime.now()
REGION_PDX = 'us-west-2'
DOMAIN_PROD = 'prod'

def test_ListLogsRequest_can_construct():
    start = NOW_DT - datetime.timedelta(days = 5)
    end = NOW_DT - datetime.timedelta(days = 1)
    context = {'username': 'jordan', 'request_time': NOW_DT,
               'start': start, 'end': end}
    request_context = ListLogsRequestContext(context, REGION_PDX, DOMAIN_PROD)
    assert request_context.start == start.isoformat()
    assert request_context.end == end.isoformat()
    assert request_context.region == REGION_PDX
    assert request_context.domain == DOMAIN_PROD
    assert request_context.request_time == NOW_DT
    assert list(request_context.dao.keys()) == ['log']
    assert request_context.dao['log'].domain == DOMAIN_PROD
    assert request_context.dao['log'].region == REGION_PDX

