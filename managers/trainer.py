from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest

from db import db
from models import UserModel, RoleType


class TrainerManager(Resource):
    @staticmethod
    def change_role(user_pk):
        user: UserModel = db.session.execute(db.select(UserModel).filter_by(pk=user_pk)).scalar_one_or_none()
        if user is None:
            raise NotFound("There is no user with this pk")
        if user.role == RoleType.trainer:
            raise BadRequest("This user is already a trainer")
        if user.role != RoleType.user:
            raise BadRequest("Only user accounts can be promoted to trainers")
        user.role = RoleType.trainer
        db.session.add(user)
        db.session.flush()
