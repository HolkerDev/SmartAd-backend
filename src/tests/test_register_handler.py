import json
import unittest
from unittest import mock

from src.functions.register.handler import register
from src.utils.aws_request import AwsRequest
from src.utils.models import User


@mock.patch("src.functions.register.handler.table")
@mock.patch("src.functions.register.handler.db")
class RegisterHandlerModuleTest(unittest.TestCase):
    @mock.patch("src.functions.register.handler.user_repository")
    def test_new_user_registration(self, repo, _, db):
        request_body = json.dumps({"email": "test@email.com", "password": "my_pass"})
        repo.find_by_email.return_value = None
        repo.create.return_value = None
        response = register(AwsRequest({"body": request_body}))
        self.assertEqual(response.status_code, 200)

    @mock.patch("src.functions.register.handler.user_repository")
    def test_new_user_email_exists(self, repo, _, db):
        request_body = json.dumps({"email": "test@email.com", "password": "my_pass"})
        repo.find_by_email.return_value = User("test@email.com")
        repo.create.return_value = None
        response = register(AwsRequest({"body": request_body}))
        self.assertEqual(response.status_code, 409)


if __name__ == "__main__":
    unittest.main()
