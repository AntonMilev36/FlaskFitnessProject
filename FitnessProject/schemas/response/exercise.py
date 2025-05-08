from marshmallow import fields, Schema, validate


class ExerciseResponseSchema(Schema):
    pk = fields.Integer()
    name = fields.String(required=True, validate=validate.And(validate.Length(min=4, max=50)))
    description = fields.String()
    video_tutorial = fields.String()


class ExerciseProgramResponse(Schema):
    pk = fields.Integer()
    name = fields.String(required=True,
                         validate=validate.And(validate.Length(min=4, max=50)))
