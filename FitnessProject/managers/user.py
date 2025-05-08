from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from managers.auth import AuthManager
from models.user import UserModel
from models.enums import RoleType


class UserManager(Resource):
    @staticmethod
    def register(user_data):
        user_data["password"] = generate_password_hash(user_data["password"], method="pbkdf2:sha256")
        user_data["role"] = RoleType.user.name
        user = UserModel(**user_data)
        db.session.add(user)
        db.session.flush()
        return AuthManager.encode_token(user)

    @staticmethod
    def login(login_data):
        user: UserModel = db.session.execute(db.select(UserModel).filter_by
                                             (email=login_data["email"])).scalar_one_or_none()
        if user is None or not check_password_hash(user.password, login_data["password"]):
            raise BadRequest("Invalid email or password")
        return AuthManager.encode_token(user)
