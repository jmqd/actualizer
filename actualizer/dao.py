import boto3
import datetime
from typing import List
from actualizer.log.base import Log
from boto3.dynamodb.conditions import Key, Attr

LOG_TABLE_NAME_TEMPLATE = 'actualizer-{region}-{domain}-logs'
ATTRIBUTE_TYPE_MAPPING = {
        'message': 'S',
        'datetime': 'S',
        'username': 'S',
        'request_time': 'S',
        'food': 'S',
        'calories': 'N'
        }

class LogTableDao:
    def __init__(self, region: str, domain: str) -> 'LogTableDao':
        self.region = region
        self.domain = domain
        self.table_name = LOG_TABLE_NAME_TEMPLATE.format(region=region, domain=domain)
        self.session = boto3.session.Session(region_name = self.region)
        self.client = self.session.client('dynamodb')
        self.ddb = self.session.resource('dynamodb')
        self.table = self.ddb.Table(self.table_name)

    def save(self, log: Log) -> None:
        itemdict = {x: getattr(x) for x in log._FIELDS}
        ddb.put_item(
                TableName = self.table_name,
                Item = convert_dict_to_ddb_item(itemdict)
                )

def list_by_timerange(self, username: str, start: datetime.datetime,
                      end: datetime.datetime) -> List[dict]:
    response = self.table.query(
            KeyConditionExpression = Key('username').eq(username) & \
            Key('datetime').gt(start) & \
            Key('datetime').lt(end)
            )
    return response

def convert_dict_to_ddb_item(data: dict) -> dict:
    return {k:{ATTRIBUTE_TYPE_MAPPING[k]: v} for k, v in data.items()}

