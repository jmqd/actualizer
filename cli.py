#!/usr/bin/env python3

import click
import datetime
from actualizer.log import client
from actualizer.api.request import LogRequestContext
from actualizer.api.request import ListLogsRequestContext
from actualizer.api import activity

# just testing
from actualizer.dao import LogTableDao
from actualizer.dao import NutritionLogDaoHelper

NOW_DT = datetime.datetime.now()
NOW = NOW_DT.isoformat()
NOW_MINUS_24HR = (NOW_DT - datetime.timedelta(hours=24)).isoformat()
NOW_MINUS_7_DAYS = (NOW_DT - datetime.timedelta(days = 7))
LOG_TABLE_NAME = 'actualizer-logs'
DEFAULT_USERNAME = 'jordan'
DEFAULT_REGION = 'us-west-2'
DEFAULT_DOMAIN = 'prod'

@click.group('cli')
def cli() -> None: pass

@cli.command('log')
@click.option('--message', '-m', type = str)
@click.option('--username', type = str, default = DEFAULT_USERNAME)
def log(**log_request: dict) -> None:
    log_request['request_time'] = NOW_DT
    log_request_context = LogRequestContext(log_request, DEFAULT_REGION, DEFAULT_DOMAIN)
    response = activity.log(log_request_context)
    print(response)

@cli.command('list')
@click.option('--username', type = str, default = DEFAULT_USERNAME)
@click.option('--start', default = NOW_MINUS_7_DAYS)
@click.option('--end', default = NOW_DT)
def list(**list_request: dict) -> None:
    list_request['request_time'] = NOW_DT
    list_request_context = ListLogsRequestContext(list_request, DEFAULT_REGION, DEFAULT_DOMAIN)
    response = activity.list(list_request_context)
    print(response)

@cli.command('test')
def test():
    context = {'username': DEFAULT_USERNAME}
    today = datetime.datetime.today() - datetime.timedelta(days = 1)
    dao = LogTableDao(DEFAULT_REGION, DEFAULT_DOMAIN)
    dao_helper = NutritionLogDaoHelper(dao, context)
    calories = dao_helper.get_calories_for_day(today)
    print(calories)

@cli.command('weekly-report')
def weekly_report():
    context = {'username': DEFAULT_USERNAME}
    today = datetime.datetime.today()
    day = today
    dao = LogTableDao(DEFAULT_REGION, DEFAULT_DOMAIN)
    dao_helper = NutritionLogDaoHelper(dao, context)

    while day > today - datetime.timedelta(days = 7):
        calories = dao_helper.get_calories_for_day(day)
        print(day, calories)
        day = day - datetime.timedelta(days = 1)

if __name__ == '__main__':
    cli()

