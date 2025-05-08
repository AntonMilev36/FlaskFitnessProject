from unittest.mock import patch
import copy

from db import db
from models import ExerciseModel, RoleType, UserModel
from services.s3 import S3Service
from tests.base import BaseAPITest
from tests.factories import UserFactory, ExerciseFactory


class TestGettingExercises(BaseAPITest):

    GET_ALL_ENDPOINT = "/exercise"
    GET_SPECIFIC_ENDPOINT = "exercise/1"

    def test_get_all_exercises_unauthenticated(self):
        self.base_unauthenticated_test(
            "get",
            self.GET_ALL_ENDPOINT
        )

    def test_get_specific_exercise_unauthenticated(self):
        self.base_unauthenticated_test(
            "get",
            self.GET_SPECIFIC_ENDPOINT,
        )

    def base_get_exercises_not_existing(self, endpoint, message):
        header = self.create_token_and_header()

        resp = self.client.get(endpoint, headers=header)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(
            resp.json,
            message
        )

    def test_get_all_exercises_not_existing(self):
        self.base_get_exercises_not_existing(
            self.GET_ALL_ENDPOINT,
            {"message": "There are no exercises created yet"}
        )

    def test_get_specific_exercises_not_existing(self):
        self.base_get_exercises_not_existing(
            self.GET_SPECIFIC_ENDPOINT,
            {"message": "There is not exercise with this pk"}
        )


    def base_get_exercises_successfully(self, endpoint, user: UserModel, ex_2=None):
        ex_1 = ExerciseFactory()

        header = self.create_token_and_header(user)

        resp = self.client.get(
            endpoint,
            headers=header
        )

        expected_fields = [
            "name",
            "description",
            "photo_tutorial",
            "pk",
            ex_1.name,
        ]

        if ex_2 is not None:
            expected_fields.append(ex_2.name)
        if user.role != RoleType.user:
            expected_fields.append("video")

        self.assertEqual(resp.status_code, 200)
        for field in expected_fields:
            self.assertIn(field, str(resp.json))

        return resp

    def test_get_all_exercises_successfully_as_user(self):
        user = UserFactory()
        exercise_2: ExerciseModel = ExerciseFactory()

        resp = self.base_get_exercises_successfully(
            self.GET_ALL_ENDPOINT,
            user,
            exercise_2
        )

        self.assertNotIn("video", str(resp.json))

    def test_get_all_exercises_successfully_as_higher_role(self):
        for role in [RoleType.super_user,
                     RoleType.trainer,
                     RoleType.admin]:
            user: UserModel = UserFactory(role=role)
            exercise_2: ExerciseModel = ExerciseFactory()

            self.base_get_exercises_successfully(
                self.GET_ALL_ENDPOINT,
                user,
                exercise_2
            )

    def test_get_specific_exercise_successfully_as_user(self):
        user = UserFactory()

        resp = self.base_get_exercises_successfully(
            self.GET_SPECIFIC_ENDPOINT,
            user
        )

        self.assertNotIn("video", str(resp.json))

    def test_get_specific_exercise_successfully_as_higher_role(self):
        for i, role in enumerate([RoleType.super_user,
                     RoleType.trainer,
                     RoleType.admin]):
            user: UserModel = UserFactory(role=role)

            self.base_get_exercises_successfully(
                f"{self.GET_SPECIFIC_ENDPOINT[:-1]}{i + 1}",
                user,
            )


class TestCreatingExercise(BaseAPITest):

    ENDPOINT = "/trainers/exercise"

    VALID_EXERCISE_DATA = {
        "name": "Bench press",
        "description": "Some description about bench pressing that comes to 50 characters",
        "tutorial_photo": "some_photo_url",
        "tutorial_extension": "png",
        "video_example": "some_video_url",
        "video_extension": "mp4",
        "author": "Kiro Breika"
    }

    def test_create_exercise_unauthenticated(self):
        self.base_unauthenticated_test(
            "post",
            self.ENDPOINT
        )
        self.objects_count_in_database(
            ExerciseModel,
            0
        )

    def test_create_exercise_unauthorized(self):
        self.base_unauthorized_test(
            "post",
            self.ENDPOINT
        )
        self.objects_count_in_database(
            ExerciseModel,
            0
        )

    def base_create_exercise_invalid_schema(self, data):
        user = UserFactory(role=RoleType.trainer)
        header = self.create_token_and_header(user)

        resp = self.client.post(
            self.ENDPOINT,
            headers=header,
            json=data
        )

        exercises = db.session.execute(
            db.select(ExerciseModel)
        ).scalars().all()

        self.assertEqual(len(exercises), 0)
        self.assert400(resp)

        return resp

    def test_create_exercise_missing_data(self):
        #Testing with empty data
        data = {}
        resp = self.base_create_exercise_invalid_schema(data)

        self.assertIn(
            "Missing data for required field.",
            str(resp.json)
        )
        self.objects_count_in_database(
            ExerciseModel,
            0
        )

    def test_create_exercise_invalid_name(self):
        #Name is too short
        data = copy.deepcopy(self.VALID_EXERCISE_DATA)
        data["name"] = "BP"

        resp = self.base_create_exercise_invalid_schema(data)
        expected_fields = [
            "name",
            "Length must be between 4 and 50."
        ]

        for field in expected_fields:
            self.assertIn(
                field,
                str(resp.json)
            )
        self.objects_count_in_database(
            ExerciseModel,
            0
        )

        #Name is too long
        data["name"] = "BP" * 26
        resp = self.base_create_exercise_invalid_schema(data)

        for field in expected_fields:
            self.assertIn(
                field,
                str(resp.json)
            )
        self.objects_count_in_database(
            ExerciseModel,
            0
        )

    def test_create_exercise_invalid_description(self):
        #Description is not long enough
        data = copy.deepcopy(self.VALID_EXERCISE_DATA)
        data["description"] = "Too short description"

        resp = self.base_create_exercise_invalid_schema(data)
        expected_fields = [
            "description",
            "Shorter than minimum length 50."
        ]

        for field in expected_fields:
            self.assertIn(
                field,
                str(resp.json)
            )
        self.objects_count_in_database(
            ExerciseModel,
            0
        )

    def test_create_exercise_invalid_author_name(self):
        #Missing last name
        data = copy.deepcopy(self.VALID_EXERCISE_DATA)
        data["author"] = "Kiro"

        resp = self.base_create_exercise_invalid_schema(data)
        expected_fields = [
            "author",
            "Need to write first and last name"
        ]

        for field in expected_fields:
            self.assertIn(field, str(resp.json))

        #Too short first name
        data["author"] = "K Breika"
        resp = self.base_create_exercise_invalid_schema(data)
        expected_fields = [
            "author",
            "First name need to be at least 2 characters"
        ]

        for field in expected_fields:
            self.assertIn(field, str(resp.json))

        # Too short last name
        data["author"] = "Kiro B"
        resp = self.base_create_exercise_invalid_schema(data)
        expected_fields = [
            "author",
            "Last name need to be at least 2 characters"
        ]

        for field in expected_fields:
            self.assertIn(field, str(resp.json))

        #Both names are too short
        data["author"] = "K B"
        resp = self.base_create_exercise_invalid_schema(data)
        expected_fields = [
            "author",
            "Both names need to be at least 2 characters"
        ]

        for field in expected_fields:
            self.assertIn(field, str(resp.json))

        #First name is too long
        data["author"] = f"{'K' * 101} Breika"
        resp = self.base_create_exercise_invalid_schema(data)
        expected_fields = [
            "author",
            "First name need to be no more than a 100 characters"
        ]

        for field in expected_fields:
            self.assertIn(field, str(resp.json))


        #Last name is too long
        data["author"] = f"Kiro {'B' * 101}"
        resp = self.base_create_exercise_invalid_schema(data)
        expected_fields = [
            "author",
            "Last name need to be no more than a 100 characters"
        ]

        for field in expected_fields:
            self.assertIn(field, str(resp.json))


        #Both names are too long
        data["author"] = f"{'K' * 101} {'B' * 101}"
        resp = self.base_create_exercise_invalid_schema(data)
        expected_fields = [
            "author",
            "Both names need to be no mere than a 100 characters"
        ]

        for field in expected_fields:
            self.assertIn(
                field,
                str(resp.json)
            )

    @patch.object(S3Service, "upload_photo", return_value="some.s3.url")
    @patch.object(S3Service, "upload_video", return_value="some.s3_video.url")
    def test_create_exercise_successfully(self, mock_s3_upload_video, mock_s3_upload_photo):
        user = UserFactory(
            role=RoleType.trainer
        )
        header = self.create_token_and_header(user)
        data = self.VALID_EXERCISE_DATA

        resp = self.client.post(
            self.ENDPOINT,
            headers=header,
            json=data
        )

        expected_fields = [
            "pk",
            "name",
            "description",
            "photo_tutorial",
            "video",
            #Checking if it's the correct exercise
            "Bench press"
        ]

        self.assertEqual(
            resp.status_code,
            201
        )
        for field in expected_fields:
            self.assertIn(
                field,
                str(resp.json)
            )

        mock_s3_upload_photo.assert_called_once()
        mock_s3_upload_video.assert_called_once()

        self.objects_count_in_database(
            ExerciseModel,
            1
        )

    def test_create_exercises_with_same_names(self):
        user = UserFactory(
            role=RoleType.trainer
        )
        header = self.create_token_and_header(user)
        data = copy.deepcopy(
            self.VALID_EXERCISE_DATA
        )

        self.client.post(
            self.ENDPOINT,
            headers=header,
            json=data
        )

        exercises = db.session.execute(
            db.select(ExerciseModel)
        ).scalars().all()

        self.assertEqual(
            len(exercises),
            1
        )

        #Using the same data, with the same names
        new_data = data

        resp = self.client.post(
            self.ENDPOINT,
            headers=header,
            json=new_data
        )

        self.assertEqual(
            resp.status_code,
            409
        )

        self.assertEqual(
            resp.json,
            {
                "message":
                    f"Exercise with name '{new_data['name']}' already exists"
            }
        )


class TestDeleteExercise(BaseAPITest):

    ENDPOINT = "/admin/delete/exercise/1"

    def test_delete_exercise_unauthenticated(self):
        ExerciseFactory()

        self.base_unauthenticated_test(
            "delete",
            self.ENDPOINT
        )
        self.objects_count_in_database(
            ExerciseModel,
            1
        )

    def test_delete_exercise_unauthorized(self):
        ExerciseFactory()

        self.base_unauthenticated_test(
            "delete",
            self.ENDPOINT
        )
        self.objects_count_in_database(
            ExerciseModel,
            1
        )

    def test_delete_non_existing_exercise(self):
        user = UserFactory(
            role=RoleType.admin
        )
        header = self.create_token_and_header(user)

        resp = self.client.delete(
            self.ENDPOINT,
            headers=header,
        )

        self.assertEqual(
            resp.status_code,
            404
        )

        self.assertEqual(
            resp.json,
            {
                "message":
                    "There is no exercise with this pk"
            }
        )


    def test_delete_exercise_successfully(self):
        exercise = ExerciseFactory()

        user = UserFactory(
            role=RoleType.admin
        )
        header = self.create_token_and_header(user)

        resp = self.client.delete(
            f"{self.ENDPOINT[:-1]}{exercise.pk}",
            headers=header,
        )

        self.assertEqual(
            resp.status_code,
            200
        )

        self.assertEqual(
            resp.json,
            {
                "message":
                    "Exercise deleted successfully"
            }
        )

        exercises = db.session.execute(
            db.select(ExerciseModel)
        ).scalars().all()

        self.assertEqual(
            len(exercises),
            0
        )
        self.objects_count_in_database(
            ExerciseModel,
            0
        )
