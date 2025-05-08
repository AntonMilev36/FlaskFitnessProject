from models import RoleType, UserModel
from tests.base import BaseAPITest
from tests.factories import UserFactory
from tests.helpers import generate_token


class TestProjectEndpoints(BaseAPITest):

    ENDPOINTS = (
        ("POST", "/trainers/exercise"),
        ("POST", "/trainers/program"),
        ("GET", "/exercise"),
        ("GET", "/program"),
        ("GET", "/exercise/1"),
        ("GET", "/program/1"),
        ("POST", "/users/add/program/1"),
        ("GET", "/user/program"),
        ("GET", "/user/program/1"),
        ("DELETE", "/admin/delete/exercise/1"),
        ("DELETE", "/admin/delete/program/1"),
        ("PUT", "/admin/trainer/1")
    )

    def make_request(self, method, url, header=None):
        if method == "GET":
            resp = self.client.get(url, headers=header)
        elif method == "POST":
            resp = self.client.post(url, headers=header)
        elif method == "PUT":
            resp = self.client.put(url, headers=header)
        else:
            resp = self.client.delete(url, headers=header)

        return resp

    def test_application_login_required_missing_token(self):
        for method, url in self.ENDPOINTS:
            resp = self.make_request(method, url)

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


    def test_application_login_required_invalid_token(self):
        header = {"Authorization": "Bearer invalid_token"}

        for method, url in self.ENDPOINTS:
            resp = self.make_request(method, url, header)

            self.assertEqual(resp.status_code, 401)
            self.assertEqual(resp.json, {
                "message": "Invalid or missing token"
            })

    def base_permissions_test(self, endpoints, user):
        user_token = generate_token(user)
        header = {
            "Authorization": f"Bearer {user_token}"
        }

        for method, url in endpoints:
            resp = self.make_request(method, url, header=header)

            self.assertEqual(resp.status_code, 403)
            self.assertEqual(
                resp.json,
                {
                    "message": "You don't have permission to do this task"
                }
            )

    def test_permissions_required_trainer(self):
        #The user is not trainer, it will throw 403 error
        endpoints = (
            ("POST", "/trainers/exercise"),
            ("POST", "/trainers/program")
        )

        user = UserFactory()

        self.base_permissions_test(endpoints, user)

    def test_permissions_required_admin(self):
        endpoints = (
            ("DELETE", "/admin/delete/exercise/1"),
            ("DELETE", "/admin/delete/program/1"),
            ("PUT", "/admin/trainer/1")
        )

        user = UserFactory()

        self.base_permissions_test(endpoints, user)

    def test_permissions_required_users(self):
        endpoints = (
            ("POST", "/users/add/program/1"),
            ("GET", "/user/program"),
            ("GET", "/user/program/1")
        )

        #Setting the user to another role, because 403 error is expected
        user = UserFactory(role=RoleType.admin)

        self.base_permissions_test(endpoints, user)


class TestRegisterSchema(BaseAPITest):

    def test_register_schema_missing_fields(self):
        data = {}

        resp = self.base_register_test(data, 400)

        required_fields = (
            "email",
            "password",
            "first_name",
            "last_name"
        )

        for curr_field in required_fields:
            self.assertIn(
                curr_field,
                resp.json["message"]
            )
        self.objects_count_in_database(
            UserModel,
            0
        )

    def base_register_invalid_field(self, date, expected_message):
        resp = self.base_register_test(date, 400)

        self.assertEqual(
            resp.json,
            expected_message
        )
        self.objects_count_in_database(
            UserModel,
            0
        )

    def test_register_schema_invalid_email(self):
        # Invalid email format
        #user = UserFactory(email="kiro")
        data = self.base_user()
        data["email"] = "kiro"

        expected_message = {
            'message': "Invalid fields {'email': ['Not a valid email address.']}"
        }

        self.base_register_invalid_field(data, expected_message)


    def test_register_schema_invalid_password(self):
        data = self.base_user()
        #Too short password
        data["password"] = "Kb1#"

        expected_message = {
            'message':
                "Invalid fields {'password': ['Password is not strong enough, try another one']}"
        }

        self.base_register_invalid_field(data, expected_message)

        data["password"] = "spas12345#" #No uppercase
        self.base_register_invalid_field(data, expected_message)

        data["password"] = "Spas#!@>?+_*" #No digits
        self.base_register_invalid_field(data, expected_message)

        data["password"] = "Spas12345" #No special chars
        self.base_register_invalid_field(data, expected_message)

        data["password"] = ("SpasSpasSpasSpasSpasSpasSpasSpasSpas"
                            "SpasSpasSpasSpasSpasSpasSpasSpasSpasSpas"
                            "SpasSpasSpasSpasSpasSpasSpasSpasSpasSpas"
                            "SpasSpasSpasSpasSpasSpasSpasSpasSpasSpas"
                            "SpasSpasSpasSpasSpasSpasSpasSpasSpasSpas"
                            "SpasSpasSpasSpasSpasSpasSpasSpasSpasSpas"
                            "SpasSpasSpasSpasSpasSpasSpasSpasSpasSpasSpas")
        expected_message = {
            'message':
                "Invalid fields {'password': ['Longer than maximum length 225.', "
                "'Password is not strong enough, try another one']}"
        }
        self.base_register_invalid_field(data, expected_message)

    def test_register_schema_invalid_names(self):
        data = self.base_user()
        #The names are too short
        data["first_name"] = "K"
        data["last_name"] = "B"

        expected_message = {
            'message':
                "Invalid fields {'first_name': ['Length must be between 2 and 100.'], "
                "'last_name': ['Length must be between 2 and 100.']}"
        }

        self.base_register_invalid_field(data, expected_message)

        data["first_name"] = "S" * 300 #Too long
        data["last_name"] = data["first_name"] #Too long
        self.base_register_invalid_field(data, expected_message)

    def test_register_database_changes(self):
        data = self.base_user()

        self.base_register_test(
            data,
            201
        )

    def test_register_duplicating_emails(self):
        data = self.base_user()

        self.base_register_test(data, 201)

        second_data = {
            "email": "kiro_the_break89@abv.bg",
            "password": "BaiToshoNumber1_1989#",
            "first_name": "Kiro",
            "last_name": "Breika"
        }

        resp = self.base_register_test(
            second_data,
            409
        )
        self.assertEqual(
            resp.json,
            {
                'message':
                    'User with this email already exist'
            }
        )


class TestLoginSchemas(BaseAPITest):

    def test_login_schema_missing_fields(self):
        data = {}

        resp = self.client.post("/login", json=data)

        expected_message = {
            'message':
                "Invalid fields {'email': ['Missing data for required field.'], "
                "'password': ['Missing data for required field.']}"
        }
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, expected_message)

    def test_login_invalid_email(self):
        #First we have to register a user
        data = self.base_user()
        self.base_register_test(data, 201)

        login_data = {
            "email": "kiro", #In wrong format
            "password": data["password"]
        }
        resp = self.client.post("/login", json=login_data)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {
            'message':
                "Invalid fields {'email': ['Not a valid email address.']}"
        })

        login_data["email"] = "kiro_breik123@abv.com"  # Valid format, but wrong

        resp = self.client.post("/login", json=login_data)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.json,
            {'message': 'Invalid email or password'}
        )

    def test_login_invalid_password(self):
        data = self.base_user()
        self.base_register_test(data, 201)

        login_data = {
            "email": data["email"],
            "password": "Tosho" #Invalid format
        }

        resp = self.client.post("/login", json=login_data)

        expected_message = {
            'message':
                "Invalid fields {'password': "
                "['Password is not strong enough, try another one']}"
        }
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, expected_message)

        login_data["password"] = "Tosho1989!"
        resp = self.client.post("/login", json=login_data)

        self.assertEqual(
            resp.status_code,
            400
        )
        self.assertEqual(
            resp.json,
            {
                "message":
                    "Invalid email or password"
            }
        )
