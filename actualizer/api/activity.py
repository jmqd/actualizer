from actualizer.api.request import LogRequestContext
from actualizer.api.request import ListLogsRequestContext
from actualizer.api.response import LogResponse
from actualizer.api.response import ListResponse

def log(request: LogRequestContext) -> LogResponse:
    return request.dao.save(request.payload)

def list(request: ListLogsRequestContext) -> ListResponse:
    return request.dao.query_by_timerange(request.username, request.start, request.end)

