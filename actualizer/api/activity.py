from actualizer.api.request import LogRequestContext
from actualizer.api.request import ListLogsRequestContext
from actualizer.api.request import ListGoalsRequestContext
from actualizer.api.response import LogResponse
from actualizer.api.response import ListResponse

def log(request: LogRequestContext) -> LogResponse:
    return request.dao['log'].save(request.log)

def list_logs(request: ListLogsRequestContext) -> ListResponse:
    return request.dao['log'].query_by_timerange(request.username, request.start, request.end)

def list_goals(request: ListGoalsRequestContext) -> ListResponse:
    return request.dao['goal'].query_by_user(request.username, request.goal_type)

