import click
import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr

NOW_DT = datetime.datetime.now()
NOW = NOW_DT.isoformat()
NOW_MINUS_24HR = (NOW_DT - datetime.timedelta(days=24)).isoformat()
LOG_TABLE_NAME = 'actualizer-logs'
DEFAULT_USERNAME = 'jordan'

ddb = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
log_table = dynamodb.Table(LOG_TABLE_NAME)

ATTRIBUTE_TYPE_MAPPING = {
        'message': 'S',
        'datetime': 'S',
        'username': 'S'
        }

@click.group('cli')
def cli() -> None: pass

@cli.command('log')
@click.option('--message', '-m', type = str)
@click.option('--datetime', type = str, default = NOW)
@click.option('--username', type = str, default = DEFAULT_USERNAME)
def log(**log_request: dict) -> None:
    _log(log_request)
    print("Put log {} to {}.".format(log_request, LOG_TABLE_NAME))

def _log(log: dict) -> None:
    ddb.put_item(
            TableName = LOG_TABLE_NAME,
            Item = convert_dict_to_ddb_item(log)
            )

@cli.command('list')
@click.option('--username', type = str, default = DEFAULT_USERNAME)
def list(**list_request: dict) -> None:
    response = _list(list_request)
    print(response['Items'])

def _list(list_request: dict) -> dict:
    username = list_request['username']
    response = log_table.query(
            KeyConditionExpression = Key('username').eq(username) & Key('datetime').gt(NOW_MINUS_24HR)
            )
    return response

def convert_dict_to_ddb_item(data: dict) -> dict:
    return {k:{ATTRIBUTE_TYPE_MAPPING[k]: v} for k, v in data.items()}

if __name__ == '__main__':
    cli()


