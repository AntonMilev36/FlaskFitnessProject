from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest

from db import db
from models import UserModel, RoleType


class TrainerManager(Resource):
    @staticmethod
    def change_role(user_pk):
        user: UserModel = db.session.execute(
            db.select(UserModel).filter_by(pk=user_pk)
        ).scalar_one_or_none()

        if user is None:
            raise NotFound(
                f"There is no user with pk={user_pk}"
            )
        if user.role == RoleType.trainer:
            raise BadRequest(
                "This user is already a trainer"
            )
        if user.role != RoleType.user:
            raise BadRequest(
                "Only user accounts can be promoted to trainers"
            )

        user.role = RoleType.trainer
        db.session.add(user)
        db.session.flush()

    @staticmethod
    def remove_trainer(trainer_pk):
        trainer = db.session.execute(
            db.select(UserModel).filter_by(pk=trainer_pk)
        ).scalar_one_or_none()

        if trainer is None:
            raise NotFound(
                f"User with pk={trainer_pk} doesn't exist"
            )

        if trainer.role != RoleType.trainer:
            raise BadRequest(
                "This user is not a trainer"
            )

        trainer.role = RoleType.user
        db.session.add(trainer)
        db.session.flush()
