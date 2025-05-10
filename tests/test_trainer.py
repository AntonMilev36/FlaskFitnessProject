from models import RoleType
from tests.base import BaseAPITest
from tests.factories import UserFactory


class TestTrainer(BaseAPITest):

    ADD_ENDPOINT = "/admin/set/trainer/9"
    REMOVE_ENDPOINT = "/admin/remove/trainer/9"

    def test_create_trainer_unauthenticated(self):
        self.base_unauthenticated_test(
            "put",
            self.ADD_ENDPOINT
        )

    def test_create_trainer_unauthorized(self):
        self.base_unauthorized_test(
            "put",
            self.ADD_ENDPOINT
        )

    def test_create_trainer_non_existing(self):
        header = self.create_token_and_header(
            UserFactory(role=RoleType.admin)
        )

        resp = self.client.put(
            self.ADD_ENDPOINT,
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
                    "There is no user with pk=9"
            }
        )

    def test_create_trainer_already_promoted(self):
        trainer = UserFactory(
            role=RoleType.trainer
        )
        header = self.create_token_and_header(
            UserFactory(role=RoleType.admin)
        )

        resp = self.client.put(
            f"{self.ADD_ENDPOINT[:-1]}{trainer.pk}",
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
                    "This user is already a trainer"
            }
        )

    def test_create_trainer_not_user(self):
        user = UserFactory(
            role=RoleType.super_user
        )
        header = self.create_token_and_header(
            UserFactory(role=RoleType.admin)
        )

        resp = self.client.put(
            f"{self.ADD_ENDPOINT[:-1]}{user.pk}",
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
                    "Only user accounts can be promoted to trainers"
            }
        )

    def test_create_trainer_successfully(self):
        user = UserFactory()
        header = self.create_token_and_header(
            UserFactory(role=RoleType.admin)
        )

        resp = self.client.put(
            f"{self.ADD_ENDPOINT[:-1]}{user.pk}",
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
                    f"User with pk={user.pk} is set to trainer"
            }
        )
        self.assertEqual(
            user.role,
            RoleType.trainer
        )

    def test_remove_trainer_unauthenticated(self):
        self.base_unauthenticated_test(
            "put",
            self.REMOVE_ENDPOINT
        )

    def test_remove_trainer_unauthorized(self):
        self.base_unauthorized_test(
            "put",
            self.REMOVE_ENDPOINT
        )

    def test_remove_trainer_non_existing(self):
        header = self.create_token_and_header(
            UserFactory(role=RoleType.admin)
        )

        resp = self.client.put(
            self.REMOVE_ENDPOINT,
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
                    "User with pk=9 doesn't exist"
            }
        )

    def test_remove_trainer_already_removed(self):
        user = UserFactory()
        header = self.create_token_and_header(
            UserFactory(role=RoleType.admin)
        )

        resp = self.client.put(
            f"{self.REMOVE_ENDPOINT[:-1]}{user.pk}",
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
                    "This user is not a trainer"
            }
        )

    def test_remove_trainer_successfully(self):
        trainer = UserFactory(
            role=RoleType.trainer
        )
        header = self.create_token_and_header(
            UserFactory(role=RoleType.admin)
        )

        resp = self.client.put(
            f"{self.REMOVE_ENDPOINT[:-1]}{trainer.pk}",
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
                    f"Trainer with pk={trainer.pk} "
                    f"is now set to user"
            }
        )
        self.assertEqual(
            trainer.role,
            RoleType.user
        )
