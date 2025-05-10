from models import RoleType, UserProgram, ProgramModel
from tests.base import BaseAPITest
from tests.factories import UserFactory, ProgramFactory


class TestAddProgramUser(BaseAPITest):

    PROG_USER_ENDPOINT = "/user/add/program/1"

    def test_add_program_to_user_unauthenticated(self):
        self.base_unauthenticated_test(
            "post",
            self.PROG_USER_ENDPOINT
        )
        self.objects_count_in_database(
            UserProgram,
            0
        )

    def test_add_program_to_user_unauthorized(self):
        self.base_unauthorized_test(
            "post",
            self.PROG_USER_ENDPOINT,
            UserFactory(role=RoleType.admin)
        )
        self.objects_count_in_database(
            UserProgram,
            0
        )

    def test_add_non_existing_program_to_user(self):
        header = self.create_token_and_header()

        resp = self.client.post(
            self.PROG_USER_ENDPOINT,
            headers=header
        )

        self.assertEqual(
            resp.status_code,
            400
        )
        self.assertEqual(
            resp.json,
            {
                "message":
                    "This program does not exist"
            }
        )
        self.objects_count_in_database(
            UserProgram,
            0
        )

    def test_add_program_to_user_twice(self):
        program = ProgramFactory()
        header = self.create_token_and_header()

        self.client.post(
            f"{self.PROG_USER_ENDPOINT[:-1]}{program.pk}",
            headers=header
        )

        resp = self.client.post(
            f"{self.PROG_USER_ENDPOINT[:-1]}{program.pk}",
            headers=header
        )

        self.assertEqual(
            resp.status_code,
            400
        )
        self.assertEqual(
            resp.json,
            {
                "message":
                    "This program is already saved"
            }
        )
        self.objects_count_in_database(
            UserProgram,
            1
        )

    def test_add_program_to_user_successfully(self):
        program = ProgramFactory()
        header = self.create_token_and_header()

        resp = self.client.post(
            f"{self.PROG_USER_ENDPOINT[:-1]}{program.pk}",
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
                    "Program is successfully added"
            }
        )


class TestGetUserPrograms(BaseAPITest):

    GET_ALL_ENDPOINT = "/user/program"
    GET_SPECIFIC_ENDPOINT = "/user/program/1"

    def test_get_all_programs_unauthenticated(self):
        self.base_unauthenticated_test(
            "get",
            self.GET_ALL_ENDPOINT
        )

    def test_get_specific_program_unauthenticated(self):
        self.base_unauthenticated_test(
            "get",
            self.GET_SPECIFIC_ENDPOINT
        )

    def test_get_all_programs_unauthorized(self):
        self.base_unauthorized_test(
            "get",
            self.GET_ALL_ENDPOINT,
            UserFactory(role=RoleType.admin)
        )

    def test_get_specific_program_unauthorized(self):
        self.base_unauthorized_test(
            "get",
            self.GET_SPECIFIC_ENDPOINT,
            UserFactory(role=RoleType.admin)
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
                    "You don't have any programs yet"
            }
        )

    def test_get_specific_programs_non_existing(self):
        self.base_get_programs_non_existing(
            self.GET_SPECIFIC_ENDPOINT,
            {
                "message":
                    "This program doesn't exist or is not added to your list"
            }
        )

    def base_get_programs_successfully(self, endpoint, prog_2):
        program: ProgramModel = ProgramFactory()
        header = self.create_token_and_header()

        self.client.post(
            f"/user/add/program/{program.pk}",
            headers=header
        )
        if endpoint == self.GET_ALL_ENDPOINT:
            self.client.post(
                f"/user/add/program/{prog_2.pk}",
                headers=header
            )

        resp = self.client.get(
            endpoint
            if endpoint == self.GET_ALL_ENDPOINT
            else f"{endpoint[:-1]}{program.pk}",
            headers=header
        )

        expected_fields = [
            "exercises",
            "name",
            "pk",
            "title",
            program.title,
            program.exercises[0].name,
            str(program.exercises[0].pk)
        ]
        if endpoint == self.GET_ALL_ENDPOINT:
            additional_fields = [
                prog_2.exercises[0].name,
                str(prog_2.exercises[0].pk),
                prog_2.title
            ]

            for field in additional_fields:
                expected_fields.append(field)

        self.assertEqual(
            resp.status_code,
            200
        )
        for field in expected_fields:
            self.assertIn(
                field,
                str(resp.json)
            )

    def test_get_all_exercises_successfully(self):
        self.base_get_programs_successfully(
            self.GET_ALL_ENDPOINT,
            ProgramFactory()
        )

    def test_get_specific_exercises_successfully(self):
        self.base_get_programs_successfully(
            self.GET_SPECIFIC_ENDPOINT,
            ProgramFactory()
        )


class TestUserDeleteProgram(BaseAPITest):

    ENDPOINT = "user/delete/program/1"
    ADD_PROGRAM_ENDPOINT = "/user/add/program/1"

    def test_delete_program_unauthenticated(self):
        self.base_unauthenticated_test(
            "delete",
            self.ENDPOINT
        )

    def test_delete_user_program_unauthorized(self):
        self.base_unauthorized_test(
            "delete",
            self.ENDPOINT,
            UserFactory(role=RoleType.admin)
        )

    def test_delete_user_non_existing_program(self):
        header = self.create_token_and_header()

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
                    "Program with pk=1 doesn't exist"
            }
        )

    def test_delete_user_program_not_in_user_list(self):
        program = ProgramFactory()
        header = self.create_token_and_header()

        resp = self.client.delete(
            f"{self.ENDPOINT[:-1]}{program.pk}",
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
                    f"This program is not in your list"
            }
        )

    def test_delete_user_program_successfully(self):
        program = ProgramFactory()
        header = self.create_token_and_header()

        #First need to add program to the user, so it can be removed
        self.client.post(
            f"{self.ADD_PROGRAM_ENDPOINT[:-1]}{program.pk}",
            headers=header
        )
        self.objects_count_in_database(
            UserProgram,
            1
        )

        resp = self.client.delete(
            f"{self.ENDPOINT[:-1]}{program.pk}",
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
                    f"Program with pk={program.pk} is deleted successfully"
            }
        )
        self.objects_count_in_database(
            UserProgram,
            0
        )
