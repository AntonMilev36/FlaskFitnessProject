from marshmallow import fields, validate

from schemas.base import BaseUserSchema


class UserRegisterSchema(BaseUserSchema):
    first_name = fields.String(required=True, validate=validate.And(validate.Length(min=2, max=100)))
    last_name = fields.String(required=True, validate=validate.And(validate.Length(min=2, max=100)))


class UserLoginSchema(BaseUserSchema):
    pass
