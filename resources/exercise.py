from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.exercise import ExerciseManager
from models import UserModel
from models.enums import RoleType
from schemas.request.exercise import CreateExerciseRequest
from schemas.response.exercise import ExerciseUserResponseSchema, ExerciseSuperUserResponseSchema
from utils.decorators import schema_validator, permission_required


class CreateExercise(Resource):
    @auth.login_required
    @permission_required([RoleType.trainer])
    @schema_validator(CreateExerciseRequest)
    def post(self):
        data = request.get_json()
        exercise = ExerciseManager.create_exercise(data)

        return ExerciseSuperUserResponseSchema().dump(
            exercise
        ), 201


class AllExercisesList(Resource):
    @auth.login_required
    def get(self):
        exercises = ExerciseManager.get_all_exercises()
        user: UserModel = auth.current_user()
        return {
            "exercises":
                ExerciseUserResponseSchema().dump(exercises, many=True)
                if user.role == RoleType.user
                else ExerciseSuperUserResponseSchema().dump(exercises, many=True)
        }


class SpecificExercise(Resource):
    @auth.login_required
    def get(self, exercise_pk):
        exercise = ExerciseManager.get_exercise(exercise_pk)
        user: UserModel = auth.current_user()
        return {
            "exercise": (
                ExerciseUserResponseSchema().dump(exercise)
                if user.role == RoleType.user
                else ExerciseSuperUserResponseSchema().dump(exercise)
            )
        }


class DeleteExercise(Resource):
    @auth.login_required
    @permission_required([RoleType.admin])
    def delete(self, exercise_pk):
        ExerciseManager.delete_exercise(exercise_pk)
        return {
            "message": "Exercise deleted successfully"
        }
