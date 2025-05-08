import os
import uuid

from flask_restful import Resource
from werkzeug.exceptions import NotFound

from constants import TEMP_FILE_FOLDER
from db import db
from models.exercise import ExerciseModel
from services.s3 import S3Service
from utils.healpers import decode_video

s3 = S3Service()

class ExerciseManager(Resource):
    @staticmethod
    def create_exercise(exercise_data):
        tutorial_video = exercise_data.pop("tutorial_video")
        tutorial_extension = exercise_data.pop("tutorial_extension")
        tutorial_key = f"{uuid.uuid4()}.{tutorial_extension}"
        full_tutorial_path = os.path.join(TEMP_FILE_FOLDER, tutorial_key)
        decode_video(full_tutorial_path, tutorial_video)
        tutorial_url = s3.upload_video(full_tutorial_path, tutorial_key, tutorial_extension)
        exercise_data["video_tutorial"] = tutorial_url
        exercise = ExerciseModel(**exercise_data)
        db.session.add(exercise)
        db.session.flush()

    @staticmethod
    def get_all_exercises():
        return db.session.execute(db.select(ExerciseModel)).scalars().all()

    @staticmethod
    def get_exercise(exercise_pk):
        exercise = db.session.execute(db.select(ExerciseModel).filter_by(pk=exercise_pk)).scalar_one_or_none()
        if exercise is None:
            raise NotFound
        return exercise
