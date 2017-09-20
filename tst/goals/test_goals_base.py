import datetime
#from actualizer.goals.base import FieldMeetsConstraintGoal

NOW = datetime.datetime.now()

def do_test_calories_goal():
    request_context = {
            'name': 'CaloriesLessThan2000Goal',
            'period': '1 day',
            'field': 'calories',
            'constraint': '< 2000',
            'request_time': datetime.datetime.now(),
            'username': 'testuser',
            }
    goal = FieldMeetsConstraintGoal(request_context)
    assert goal.name == request_context['name']
    assert goal.period == request_context['period']
    assert goal.field == request_context['field']
    assert goal.constraint == request_context['constraint']
    assert goal.created == request_context['created']
    assert goal.updated == request_context['updated']

