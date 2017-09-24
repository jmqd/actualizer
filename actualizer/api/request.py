from actualizer.dao import LogTableDao
from actualizer.dao import GoalTableDao
from actualizer.log import client

'''TODO:
    1. Create a class to abstract all the super().__init__ stuff away.
        Something that abstracts the idea of "request-specific fields".
'''

DAOS = {
        'log': LogTableDao,
        'goal': GoalTableDao
        }

class RequestContext:
    def __init__(self, payload: dict, region: str, domain: str) -> 'RequestContext':
        self.region = region
        self.domain = domain
        self.username = payload['username']
        self.request_time = payload['request_time']
        self.dao = {k:DAOS[k](self.region, self.domain) for k in self.__class__.REQUIRED_DAOS}

    def __str__(self) -> str:
        return '{}[{}][{}]: {}'.format(self.__class__.__name__, self.region, self.domain, self.request)

class LogDaoRequest(RequestContext):
    REQUIRED_DAOS = {'log'}

class GoalDaoRequest(RequestContext):
    REQUIRED_DAOS = {'goal'}

class LogRequestContext(LogDaoRequest):
    def __init__(self, payload: dict, region: str, domain: str) -> None:
        super().__init__(payload, region, domain)
        self.log = client.factory(payload)

class ListLogsRequestContext(LogDaoRequest):
    def __init__(self, payload: dict, region: str, domain: str) -> None:
        super().__init__(payload, region, domain)
        self.start = payload['start'].isoformat()
        self.end = payload['end'].isoformat()

class ListGoalsRequestContext(GoalDaoRequest):
    def __init__(self, payload: dict, region: str, domain: str) -> None:
        super().__init__(payload, region, domain)
        self.goal_type = payload.get('goal_type')

