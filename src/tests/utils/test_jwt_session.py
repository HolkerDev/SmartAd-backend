import unittest

from src.utils.jwt_session import generate_token, is_valid_token


class JwtSessionModuleTest(unittest.TestCase):
    def test_jwt_validation_and_creation_works_OK(self):
        token = generate_token({"email": "test@email.com"})
        self.assertTrue(is_valid_token(token=token))

    def test_jwt_validation_returns_false_when_jwt_wrong(self):
        self.assertFalse(is_valid_token("wrong_token"))


if __name__ == "__main__":
    unittest.main()
