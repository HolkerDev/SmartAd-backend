import json
import unittest
from unittest import mock
from src.functions.login.handler import login

from src.utils.aws_request import AwsRequest
from src.utils.models import FullUser
from src.utils.password import hash_password


class LoginHandlerModuleTest(unittest.TestCase):
    def test_login_with_wrong_body(self):
        request_body = json.dumps({"wrong_body": "test"})
        response = login(AwsRequest({"body": request_body}))
        self.assertEqual(response.status_code, 400)

    def test_login_with_empty_body(self):
        request_body = json.dumps({})
        response = login(AwsRequest({"body": request_body}))
        self.assertEqual(response.status_code, 400)

    @mock.patch("src.functions.login.handler.user_repository")
    def test_login_with_wrong_password(self, repo):
        request_body = json.dumps({"email": "test@email.com", "password": "12345"})
        repo.find_by_email_f.return_value = FullUser(
            "test@email.com", "wrong_pass".encode()
        )
        response = login(AwsRequest({"body": request_body}))
        self.assertEqual(response.status_code, 401)

    @mock.patch("src.functions.login.handler.user_repository")
    def test_login_with_wrong_email(self, repo):
        request_body = json.dumps({"email": "test@email.com", "password": "12345"})
        repo.find_by_email_f.return_value = None
        response = login(AwsRequest({"body": request_body}))
        self.assertEqual(response.status_code, 401)

    @mock.patch("src.functions.login.handler.user_repository")
    def test_login_with_OK_body(self, repo):
        request_body = json.dumps({"email": "test@email.com", "password": "12345"})
        repo.find_by_email_f.return_value = FullUser(
            email="tset@email.com", password=hash_password("12345")
        )
        response = login(AwsRequest({"body": request_body}))
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
