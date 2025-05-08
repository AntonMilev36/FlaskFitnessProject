import os
import uuid

from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, Conflict

from constants import TEMP_FILE_FOLDER
from db import db
from models.exercise import ExerciseModel
from services.s3 import S3Service
from utils.healpers import decode_photo, decode_video

s3 = S3Service()


class ExerciseManager(Resource):
    @staticmethod
    def create_exercise(exercise_data):
        tutorial_photo = exercise_data.pop("tutorial_photo")
        tutorial_extension = exercise_data.pop("tutorial_extension")

        tutorial_key = f"{uuid.uuid4()}.{tutorial_extension}"
        full_tutorial_path = os.path.join(TEMP_FILE_FOLDER, tutorial_key)
        decode_photo(full_tutorial_path, tutorial_photo)

        tutorial_url = s3.upload_photo(
            full_tutorial_path, tutorial_key, tutorial_extension
        )
        exercise_data["photo_tutorial"] = tutorial_url

        video_example = exercise_data.pop("video_example")
        video_extension = exercise_data.pop("video_extension")
        if video_example and video_extension:
            video_key = f"{uuid.uuid4()}.{video_extension}"
            full_video_path = os.path.join(TEMP_FILE_FOLDER, video_key)
            decode_video(full_video_path, video_example)
            video_url = s3.upload_video(full_video_path, video_key, video_extension)
            exercise_data["video"] = video_url

        exercise: ExerciseModel = ExerciseModel(**exercise_data)

        try:
            db.session.add(exercise)
            db.session.flush()
        except IntegrityError:
            raise Conflict(
                f"Exercise with name '{exercise.name}' already exists"
            )
        else:
            return exercise

    @staticmethod
    def get_all_exercises():
        exercises = db.session.execute(
            db.select(ExerciseModel)
        ).scalars().all()

        if not exercises:
            raise NotFound(
                "There are no exercises created yet"
            )

        return exercises

    @staticmethod
    def get_exercise(exercise_pk):
        exercise = db.session.execute(
            db.select(ExerciseModel).filter_by(pk=exercise_pk)
        ).scalar_one_or_none()
        if exercise is None:
            raise NotFound("There is not exercise with this pk")
        return exercise

    @staticmethod
    def delete_exercise(exercise_pk):
        exercise = db.session.execute(
            db.select(ExerciseModel).filter_by(pk=exercise_pk)
        ).scalar_one_or_none()
        if exercise is None:
            raise NotFound("There is no exercise with this pk")
        db.session.delete(exercise)
        db.session.flush()
