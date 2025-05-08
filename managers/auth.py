from datetime import datetime, timedelta, timezone

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import Unauthorized

from db import db
from models import UserModel


class AuthManager:
    @staticmethod
    def encode_token(user: UserModel):
        data = {
            "sub": user.pk,
            "exp": datetime.now(timezone.utc) + timedelta(days=5),
            "role": user.role if isinstance(user.role, str) else user.role.name
        }
        key = config("SECRET_KEY")
        new_token = jwt.encode(data, key=key, algorithm="HS256")
        return {"token": new_token}

    @staticmethod
    def decode_token(token):
        try:
            key = config("SECRET_KEY")
            user = jwt.decode(token, key=key, algorithms=["HS256"])
        except:
            raise jwt.exceptions.InvalidTokenError
        else:
            return user["sub"], user["role"]


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    try:
        user_pk, user_role = AuthManager.decode_token(token)
        user = db.session.execute(db.select(UserModel).filter_by(pk=user_pk)).scalar()
    except jwt.exceptions.InvalidTokenError:
        raise Unauthorized("Invalid or missing token")
    else:
        return user
