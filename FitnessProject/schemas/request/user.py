from marshmallow import Schema, fields, validate
from utils.validators import validate_email, password_validator


class BaseUserSchema(Schema):
    email = fields.String(required=True, validate=validate_email)
    password = fields.String(required=True,
                             validate=validate.And(validate.Length(max=225),
                                                   password_validator))


class UserRegisterSchema(BaseUserSchema):
    first_name = fields.String(required=True, validate=validate.And(validate.Length(min=2, max=100)))
    last_name = fields.String(required=True, validate=validate.And(validate.Length(min=2, max=100)))


class UserLoginSchema(BaseUserSchema):
    pass
