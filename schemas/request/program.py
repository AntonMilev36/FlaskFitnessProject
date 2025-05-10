from marshmallow import fields

from schemas.base import BaseProgramSchema
from schemas.request.exercise import ExerciseProgramRequest

"""
    It uses this nested schema to give
    only pk, when creating program
"""


class ProgramRequestSchema(BaseProgramSchema):
    exercises = fields.List(
        fields.Nested(ExerciseProgramRequest),
        required=True
    )
