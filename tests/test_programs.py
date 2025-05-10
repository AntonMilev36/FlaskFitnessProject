import copy

from models import RoleType, ProgramModel, ProgramExercise
from tests.base import BaseAPITest
from tests.factories import UserFactory, ExerciseFactory, ProgramFactory


class TestCreateProgram(BaseAPITest):

    ENDPOINT = "/trainers/program"

    VALID_PROGRAM_DATA = {
        "title": "Legs",
        "exercises": [
            {"pk": 1}
        ]
    }

    def test_create_program_unauthenticated(self):
        self.base_unauthenticated_test(
            "post",
            self.ENDPOINT
        )
        self.objects_count_in_database(
            ProgramModel,
            0
        )

    def test_create_program_unauthorized(self):
        self.base_unauthorized_test(
            "post",
            self.ENDPOINT
        )
        self.objects_count_in_database(
            ProgramModel,
            0
        )

    def base_program_schema_test(self, data):
        user = UserFactory(
            role=RoleType.trainer
        )
        header = self.create_token_and_header(user)

        resp = self.client.post(
            self.ENDPOINT,
            headers=header,
            json=data
        )

        return resp

    def test_program_schema_missing_data(self):
        data = {}

        resp = self.base_program_schema_test(data)

        expected_fields = [
            "Missing data for required field.",
            "title",
            "exercises"
        ]

        self.assertEqual(resp.status_code, 400)

        for field in expected_fields:
            self.assertIn(field, str(resp.json))

        self.objects_count_in_database(
            ProgramModel,
            0
        )

    def test_program_schema_invalid_title(self):
        data = copy.deepcopy(
            self.VALID_PROGRAM_DATA
        )
        #Title is too short
        data["title"] = "Le"

        resp = self.base_program_schema_test(data)

        expected_fields = [
            "title",
            "Length must be between 3 and 50."
        ]

        self.assertEqual(
            resp.status_code,
            400
        )

        for field in expected_fields:
            self.assertIn(
                field,
                str(resp.json)
            )
        self.objects_count_in_database(
            ProgramModel,
            0
        )

        #Title is too long
        data["title"] = "Legs" * 13

        resp = self.base_program_schema_test(data)

        self.assertEqual(
            resp.status_code,
            400
        )
        for field in expected_fields:
            self.assertIn(
                field,
                str(resp.json)
            )
        self.objects_count_in_database(
            ProgramModel,
            0
        )
        self.objects_count_in_database(
            ProgramExercise,
            0
        )

    def test_create_program_with_non_existing_exercise(self):
        user = UserFactory(
            role=RoleType.trainer
        )
        header = self.create_token_and_header(user)

        resp = self.client.post(
            self.ENDPOINT,
            headers=header,
            json=self.VALID_PROGRAM_DATA
        )

        self.assertEqual(
            resp.status_code,
            404
        )

        self.assertEqual(
            resp.json,
            {
                "message":
                    "Exercise with pk=1 does not exist"
            }
        )

        self.objects_count_in_database(
            ProgramModel,
            0
        )
        self.objects_count_in_database(
            ProgramExercise,
            0
        )

    def test_create_program_successfully(self):
        exercise = ExerciseFactory()
        user = UserFactory(
            role=RoleType.trainer
        )
        header = self.create_token_and_header(user)
        data = copy.deepcopy(self.VALID_PROGRAM_DATA)
        data["exercises"] = [{"pk": exercise.pk}]

        resp = self.client.post(
            self.ENDPOINT,
            headers=header,
            json=data
        )

        expected_fields = [
            "title",
            "exercises",
            "program",
            exercise.name,
            str(exercise.pk),
            data["title"]
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
        self.objects_count_in_database(
            ProgramModel,
            1
        )
        self.objects_count_in_database(
            ProgramExercise,
            1
        )


class GetPrograms(BaseAPITest):

    GET_ALL_ENDPOINT = "/program"
    GET_SPECIFIC_ENDPOINT = "/program/1"

    def test_get_all_programs_unauthenticated(self):
        self.base_unauthenticated_test(
            "get",
            self.GET_ALL_ENDPOINT
        )

    def test_get_specific_programs_unauthenticated(self):
        self.base_unauthenticated_test(
            "get",
            self.GET_SPECIFIC_ENDPOINT,
        )

    def base_get_programs_non_existing(self, endpoint, message):
        header = self.create_token_and_header()

        resp = self.client.get(
            endpoint,
            headers=header
        )

        self.assertEqual(
            resp.status_code,
            404
        )

        self.assertEqual(
            resp.json,
            message
        )

    def test_get_all_programs_non_existing(self):
        self.base_get_programs_non_existing(
            self.GET_ALL_ENDPOINT,
            {
                "message":
                    "There are no programs created yet!"
            }
        )

    def test_get_specific_program_non_existing(self):
        self.base_get_programs_non_existing(
            self.GET_SPECIFIC_ENDPOINT,
            {
                "message":
                    "This program does not exist"
            }
        )

    def base_get_program_successfully(self, endpoint, program_2=None):
        header = self.create_token_and_header()

        program = ProgramFactory()

        resp = self.client.get(
            endpoint,
            headers=header
        )

        expected_fields = [
            "title",
            "exercises",
            f"'pk': {program.pk}",
            "name"
        ]

        if program_2 is not None:
            additional_fields = [
                "programs",
                f"'pk': {program_2.pk}"
            ]

            for field in additional_fields:
                expected_fields.append(
                    field
                )

        self.assertEqual(
            resp.status_code,
            200
        )

        for field in expected_fields:
            self.assertIn(
                field,
                str(resp.json)
            )

        return program.pk

    def test_get_all_programs_successfully(self):
        program_2 = ProgramFactory()

        self.base_get_program_successfully(
            self.GET_ALL_ENDPOINT,
            program_2
        )

    def test_get_specific_program_successfully(self):
        self.base_get_program_successfully(
            self.GET_SPECIFIC_ENDPOINT
        )


class TestDeletePrograms(BaseAPITest):

    ENDPOINT = "admin/delete/program/1"

    def test_delete_program_unauthenticated(self):
        ProgramFactory()

        self.base_unauthenticated_test(
            "delete",
            self.ENDPOINT
        )
        self.objects_count_in_database(
            ProgramModel,
            1
        )

    def test_delete_program_unauthorized(self):
        ProgramFactory()

        self.base_unauthorized_test(
            "delete",
            self.ENDPOINT
        )
        self.objects_count_in_database(
            ProgramModel,
            1
        )

    def test_delete_program_non_existing(self):
        user = UserFactory(
            role=RoleType.admin
        )
        header = self.create_token_and_header(user)

        resp = self.client.delete(
            self.ENDPOINT,
            headers=header
        )

        self.assertEqual(
            resp.status_code,
            404
        )

        self.assertEqual(
            resp.json,
            {
                "message":
                    "Program with pk=1 does not exist"
            }
        )

    def test_delete_program_successfully(self):
        program = ProgramFactory()
        user = UserFactory(
            role=RoleType.admin
        )
        header = self.create_token_and_header(user)

        resp = self.client.delete(
            f"/admin/delete/program/{program.pk}",
            headers=header
        )

        self.assertEqual(
            resp.status_code,
            200
        )

        self.assertEqual(
            resp.json,
            {
                "message":
                    "Program is deleted successfully"
            }
        )

        self.objects_count_in_database(
            ProgramModel,
            0
        )
