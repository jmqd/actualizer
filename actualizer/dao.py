import boto3
import datetime
from typing import List
from inspect import signature
from actualizer import log
from actualizer import util
from boto3.dynamodb.conditions import Key, Attr

LOG_TABLE_NAME_TEMPLATE = 'actualizer-{region}-{domain}-logs'
LOG_SUBCLASSES = [x for x in util.get_all_subclasses(log.base.Log)]
FIELD_SERIALIZERS = {k:v for x in LOG_SUBCLASSES for k, v in x.FIELD_SERIALIZER.items()}

# mapping from field name to serializer function return type
RETURN_SIGNATURES_FOR_FIELDS = {k:signature(v).return_annotation for k, v in FIELD_SERIALIZERS.items()}

# mapping from return types to DDB string codes for that type
DDB_ATTRIBUTE_TYPE_MAPPING = {
        str: 'S',
        int: 'N',
        float: 'N'
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

    def save(self, log: log.base.Log) -> None:
        itemdict = log.to_serialized_dict()
        put_response = self.client.put_item(
                TableName = self.table_name,
                Item = convert_dict_to_ddb_item(itemdict)
                )
        return put_response

    def query_by_timerange(self, username: str, start: datetime.datetime,
                          end: datetime.datetime) -> List[dict]:
        response = self.table.query(
                KeyConditionExpression = Key('username').eq(username) & \
                Key('datetime').between(start, end)
                )
        return response

class NutritionLogDaoHelper:
    def __init__(self, dao: LogTableDao, context: dict):
        self.dao = dao
        self.context = context

    def get_calories_for_day(self, day: datetime.datetime) -> int:
        start = day.isoformat()
        end = (day + datetime.timedelta(days = 1)).isoformat()
        response = self.dao.query_by_timerange(self.context['username'], start, end)
        items = response['Items']
        calories = sum([x.get('calories', 0) for x in items])
        return calories

def convert_dict_to_ddb_item(data: dict) -> dict:
    return {k:{DDB_ATTRIBUTE_TYPE_MAPPING[RETURN_SIGNATURES_FOR_FIELDS[k]]: v} for k, v in data.items()}

