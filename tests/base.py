from flask_testing import TestCase

from config import create_app
from db import db
from tests.factories import UserFactory
from tests.helpers import generate_token


class BaseAPITest(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def base_register_test(self, data, status_code):

        resp = self.client.post("/register", json=data)

        self.assertEqual(resp.status_code, status_code)

        return resp

    @staticmethod
    def base_user():
        return {
            "email": "kiro_the_break89@abv.bg",
            "password": "BaiTosho1989#",
            "first_name": "Kiro",
            "last_name": "Breika"
        }

    def base_unauthenticated_test(self, method, endpoint):
        if method == "get":
            resp = self.client.get(endpoint)
        elif method == "post":
            resp = self.client.post(endpoint)
        elif method == "put":
            resp = self.client.put(endpoint)
        else:
            resp = self.client.delete(endpoint)

        self.assertEqual(
            resp.status_code,
            401
        )
        self.assertEqual(
            resp.json,
            {
                "message": "Invalid or missing token"
            }
        )

    def base_unauthorized_test(self, method, endpoint, user=None):
        header = self.create_token_and_header(user)

        if method == "get":
            resp = self.client.get(
                endpoint,
                headers=header
            )
        elif method == "post":
            resp = self.client.post(
                endpoint,
                headers=header
            )
        elif method == "put":
            resp = self.client.put(
                endpoint,
                headers=header
            )
        else:
            resp = self.client.delete(
                endpoint,
                headers=header
            )

        self.assertEqual(
            resp.status_code,
            403
        )

        self.assertEqual(
            resp.json,
            {
                "message":
                    "You don't have permission to do this task"
            }
        )

    @staticmethod
    def create_token_and_header(user=None):
        if user is None:
            user = UserFactory()

        user_token = generate_token(user)
        header = {
            "Authorization": f"Bearer {user_token}"
        }

        return header

    def objects_count_in_database(self, model_class, expected_count):
        programs = db.session.execute(
            db.select(model_class)
        ).scalars().all()

        self.assertEqual(
            len(programs),
            expected_count
        )
