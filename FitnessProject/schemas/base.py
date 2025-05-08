from marshmallow import Schema, fields, validate


class BaseProgramSchema(Schema):
    title = fields.String(required=True, validate=validate.And(validate.Length(min=3, max=50)))
