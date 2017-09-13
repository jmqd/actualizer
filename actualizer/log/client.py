from typing import List
import datetime
import re
import util
import base

LOG_SUBCLASSES = util.get_all_subclasses(base.Log)

def factory(log_request_context: dict) -> Log:
    kind = get_log_type(log['message'])
    return kind(log_request_context)

def get_log_type(message: str) -> type:
    for cls in LOG_SUBCLASSES:
        if cls.LOG_PATTERN.match(message):
            return cls
    return None

