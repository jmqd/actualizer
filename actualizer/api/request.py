from actualizer.dao import LogTableDao
from actualizer.log import client

class RequestContext:
    def __str__(self) -> str:
        return '{}[{}][{}]: {}'.format(self.__class__.__name__, self.region, self.domain, self.request)

class LogRequestContext(RequestContext):
    def __init__(self, payload: dict, region: str, domain: str) -> RequestContext:
        self.payload = client.factory(payload)
        self.region = region
        self.domain = domain
        self.dao = LogTableDao(self.region, self.domain)

