from flask_restful import Resource

from managers.auth import auth
from managers.user import UserManager
from models import RoleType
from schemas.response.program import ProgramResponseSchema
from utils.decorators import permission_required


class AddProgramToUser(Resource):
    @auth.login_required
    @permission_required([RoleType.user, RoleType.super_user])
    def post(self, program_pk):
        user = auth.current_user()
        UserManager.add_program(user, program_pk)
        return {
            "message":
                "Program is successfully added"
        }


class UserProgramsList(Resource):
    @auth.login_required
    @permission_required([RoleType.user, RoleType.super_user])
    def get(self):
        user = auth.current_user()
        programs = UserManager.get_all_user_programs(user)
        return ProgramResponseSchema().dump(
            programs, many=True
        )


class UserSpecificProgram(Resource):
    @auth.login_required
    @permission_required([RoleType.user, RoleType.super_user])
    def get(self, program_pk):
        user = auth.current_user()
        program = UserManager.get_specific_program(
            user,
            program_pk
        )

        return ProgramResponseSchema().dump(program)


class UserDeleteProgram(Resource):
    @auth.login_required
    @permission_required([RoleType.user, RoleType.super_user])
    def delete(self, program_pk):
        user = auth.current_user()
        UserManager.user_delete_program(
            program_pk,
            user
        )

        return {
            "message":
                f"Program with pk={program_pk} is deleted successfully"
        }
