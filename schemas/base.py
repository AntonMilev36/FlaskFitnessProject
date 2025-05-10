from marshmallow import Schema, fields, validate

from utils.validators import password_validator  # , validate_email


class BaseUserSchema(Schema):
    email = fields.Email(
        required=True
    )
    password = fields.String(
        required=True,
        validate=validate.And(
            validate.Length(max=225),
            password_validator)
    )


class BaseProgramSchema(Schema):
    title = fields.String(
        required=True,
        validate=validate.And(
            validate.Length(min=3, max=50)
        )
    )
