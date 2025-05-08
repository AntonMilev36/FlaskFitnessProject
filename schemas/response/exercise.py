from marshmallow import fields, Schema, validate


class ExerciseUserResponseSchema(Schema):
    pk = fields.Integer()
    name = fields.String()
    description = fields.String()
    photo_tutorial = fields.URL()


class ExerciseSuperUserResponseSchema(ExerciseUserResponseSchema):
    video = fields.URL()


class ExerciseProgramResponse(Schema):
    pk = fields.Integer()
    name = fields.String(required=True,
                         validate=validate.And(validate.Length(min=4, max=50)))
