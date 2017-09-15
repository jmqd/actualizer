import click
import datetime
from actualizer.log import client
from actualizer.api.request import LogRequestContext
from actualizer.api import activity

NOW_DT = datetime.datetime.now()
NOW = NOW_DT.isoformat()
NOW_MINUS_24HR = (NOW_DT - datetime.timedelta(days=24)).isoformat()
LOG_TABLE_NAME = 'actualizer-logs'
DEFAULT_USERNAME = 'jordan'
DEFAULT_REGION = 'us-west-2'
DEFAULT_DOMAIN = 'prod'

@click.group('cli')
def cli() -> None: pass

@cli.command('log')
@click.option('--message', '-m', type = str)
@click.option('--request-time', type = str, default = NOW_DT)
@click.option('--username', type = str, default = DEFAULT_USERNAME)
def log(**log_request: dict) -> None:
    log_request_context = LogRequestContext(log_request, DEFAULT_REGION, DEFAULT_DOMAIN)
    response = activity.log(log_request_context)
    print(response)

@cli.command('list')
@click.option('--username', type = str, default = DEFAULT_USERNAME)
def list(**list_request: dict) -> None:
    response = _list(list_request)
    print(response['Items'])

if __name__ == '__main__':
    cli()

