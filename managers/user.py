from flask_restful import Resource
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from managers.auth import AuthManager
from models import ProgramModel, UserProgram
from models.enums import RoleType
from models.user import UserModel


class UserManager(Resource):
    @staticmethod
    def register(user_data):
        user_data["password"] = generate_password_hash(user_data["password"], method="pbkdf2:sha256")
        user_data["role"] = RoleType.user.name
        user = UserModel(**user_data)

        try:
            db.session.add(user)
            db.session.flush()
        except Exception:
            raise Conflict("User with this email already exist")
        else:
            return AuthManager.encode_token(user)

    @staticmethod
    def login(login_data):
        user: UserModel = db.session.execute(db.select(UserModel).filter_by
                                             (email=login_data["email"])).scalar_one_or_none()
        if user is None or not check_password_hash(user.password, login_data["password"]):
            raise BadRequest("Invalid email or password")
        return AuthManager.encode_token(user)

    @staticmethod
    def add_program(user: UserModel, program_pk):
        program: ProgramModel = db.session.execute(db.select(ProgramModel).filter_by
                                                   (pk=program_pk)).scalar_one_or_none()
        if program is None:
            raise BadRequest("This program does not exist")

        if program in user.programs:
            raise BadRequest("This program is already saved")

        user.programs.append(program)
        db.session.flush()

    @staticmethod
    def get_all_user_programs(user: UserModel):
        programs = user.programs

        if not programs:
            raise NotFound(
                "You don't have any programs yet"
            )

        return programs

    @staticmethod
    def get_specific_program(user: UserModel, program_pk):
        program = [p for p in user.programs if p.pk == program_pk]

        if not program:
            raise NotFound(
                "This program doesn't exist or is not added to your list"
            )

        return program.pop()

    @staticmethod
    def user_delete_program(program_pk, user):
        program = db.session.execute(
            db.select(ProgramModel).filter_by(pk=program_pk)
        ).scalar_one_or_none()

        if program is None:
            raise NotFound(
                f"Program with pk={program_pk} doesn't exist"
            )

        user_program = db.session.execute(
            db.select(UserProgram).filter_by(
                user_pk=user.pk,
                program_pk=program_pk
            )
        ).scalar_one_or_none()

        if user_program is None:
            raise NotFound(
                "This program is not in your list"
            )

        db.session.delete(user_program)
        db.session.flush()

