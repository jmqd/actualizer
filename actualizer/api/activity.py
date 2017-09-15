from actualizer.api.request import LogRequestContext
from actualizer.api.response import LogResponse

def log(request: LogRequestContext) -> LogResponse:
    return request.dao.save(request.payload)

