from flask import request
from flask_restful import Resource

from managers.user import UserManager
from schemas.request.user import UserRegisterSchema, UserLoginSchema
from utils.decorators import schema_validator


class RegisterUser(Resource):
    @staticmethod
    @schema_validator(UserRegisterSchema)
    def post():
        data = request.get_json()
        new_user = UserManager.register(data)
        return new_user, 201


class LoginUser(Resource):
    @staticmethod
    @schema_validator(UserLoginSchema)
    def post():
        data = request.get_json()
        user = UserManager.login(data)
        return user
