from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.exercise import ExerciseManager
from models.enums import RoleType
from schemas.request.exercise import CreateExerciseRequest
from schemas.response.exercise import ExerciseResponseSchema
from utils.decorators import schema_validator, permission_required


class CreateExercise(Resource):
    @auth.login_required
    @schema_validator(CreateExerciseRequest)
    @permission_required(RoleType.trainer)
    def post(self):
        data = request.get_json()
        ExerciseManager.create_exercise(data)
        return 201


class AllExercisesList(Resource):
    @auth.login_required
    def get(self):
        exercises = ExerciseManager.get_all_exercises()
        return {"exercises": ExerciseResponseSchema().dump(exercises, many=True)}


class SpecificExercise(Resource):
    @auth.login_required
    def get(self, exercise_pk):
        exercise = ExerciseManager.get_exercise(exercise_pk)
        return ExerciseResponseSchema().dump(exercise)
