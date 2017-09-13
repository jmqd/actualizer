from typing import List
import datetime
import re

from actualizer import util
from actualizer.log import base

LOG_SUBCLASSES = util.get_all_subclasses(base.Log)

def factory(log_request_context: dict) -> base.Log:
    kind = get_log_type(log['message'])
    return kind(log_request_context)

def get_log_type(message: str) -> type:
    for cls in LOG_SUBCLASSES:
        if cls.MESSAGE_PATTERN.match(message):
            return cls
    return None

