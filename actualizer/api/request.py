from actualizer.dao import LogTableDao
from actualizer.log import client

class RequestContext:
    def __init__(self, payload: dict, region: str, domain: str) -> 'RequestContext':
        self.region = region
        self.domain = domain
        self.username = payload['username']
        self.request_time = payload['request_time']

    def __str__(self) -> str:
        return '{}[{}][{}]: {}'.format(self.__class__.__name__, self.region, self.domain, self.request)

class LogDaoRequest(RequestContext):
    def __init__(self, payload: dict, region: str, domain: str) -> 'RequestContext':
        super().__init__(payload, region, domain)
        self.dao = LogTableDao(self.region, self.domain)

class LogRequestContext(LogDaoRequest):
    def __init__(self, payload: dict, region: str, domain: str) -> RequestContext:
        super().__init__(payload, region, domain)
        self.payload = client.factory(payload)

class ListLogsRequestContext(LogDaoRequest):
    def __init__(self, payload: dict, region: str, domain: str) -> RequestContext:
        super().__init__(payload, region, domain)
        self.start = payload['start'].isoformat()
        self.end = payload['end'].isoformat()

