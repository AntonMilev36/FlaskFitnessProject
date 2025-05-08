from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.program import ProgramManager
from models.enums import RoleType
from schemas.request.program import ProgramRequestSchema
from schemas.response.program import ProgramResponseSchema
from utils.decorators import schema_validator, permission_required


class CreateProgram(Resource):
    @auth.login_required
    @permission_required([RoleType.trainer])
    @schema_validator(ProgramRequestSchema)
    def post(self):
        data = request.get_json()
        program = ProgramManager.create_program(data)
        return {"program": ProgramResponseSchema().dump(program)}, 201


class AllProgramsList(Resource):
    @auth.login_required
    def get(self):
        programs = ProgramManager.get_all_programs()
        return {"programs": ProgramResponseSchema().dump(programs, many=True)}


class SpecificProgram(Resource):
    @auth.login_required
    def get(self, program_pk):
        program = ProgramManager.get_program(program_pk)
        return ProgramResponseSchema().dump(program)


class DeleteProgram(Resource):
    @auth.login_required
    @permission_required([RoleType.admin])
    def delete(self, program_pk):
        ProgramManager.delete_program(
            program_pk
        )

        return {
            "message":
                "Program is deleted successfully"
        }
