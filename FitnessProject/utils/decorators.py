from flask import request
from marshmallow import Schema
from werkzeug.exceptions import Forbidden, BadRequest

from managers.auth import auth
from models.user import UserModel


def permission_required(required_role):
    def decorator(function):
        def wrapper(*args, **kwargs):
            user: UserModel = auth.current_user()
            if user.role != required_role:
                raise Forbidden("You don't have permission to do this task")
            return function(*args, **kwargs)
        return wrapper
    return decorator

def schema_validator(schema_name):
    def decorator(function):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            schema: Schema = schema_name()
            errors = schema.validate(data)
            if errors:
                raise BadRequest(f"Invalid fields {errors}")
            return function(*args, **kwargs)
        return wrapper
    return decorator
