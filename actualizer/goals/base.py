import datetime
from actualizer import util
from actualizer.goals.serializers import *

class Goal:
    FIELDS = ['username', 'created', 'updated', 'goal_type', 'name']
    FIELD_SERIALIZER = {k:eval('serialize_{}'.format(k)) for k in FIELDS}

    def __init__(self, request_context: dict) -> 'Log':
        self.username = request_context['username']
        self.created = request_context['request_time']
        self.updated = request_context['request_time']
        self.name = request_context['name']

    @property
    def goal_type(self):
        return self.__class__.__name__

    def to_serialized_dict(self) -> dict:
        return {k: self.FIELD_SERIALIZER[k](getattr(self, k)) for k in self.FIELDS}

