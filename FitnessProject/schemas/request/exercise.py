from marshmallow import Schema, fields, validate

from utils.validators import validate_name


class CreateExerciseRequest(Schema):
    name = fields.String(required=True, validate=validate.And(validate.Length(min=4, max=50)))
    description = fields.String(required=True, validate=validate.And(validate.Length(min=50)))
    tutorial_video = fields.String(required=True)
    tutorial_extension = fields.String(required=True)
    author = fields.String(required=True, validate=validate_name)


class ExerciseProgramRequest(Schema):
    pk = fields.Integer(required=True)
