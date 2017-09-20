from actualizer.goals.base import Goal

class FieldMeetsConstraintGoal(Goal):
    FIELDS = ['field', 'constraint']

    def __init__(self, request_context: dict) -> None:
        super().__init__(request_context)
        self.field = request_context['field']
        self.constraint = request_context['constraint']


