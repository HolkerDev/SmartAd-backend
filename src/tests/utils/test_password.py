import unittest

from src.utils.password import hash_password, is_password_equals


class PasswordModuleTest(unittest.TestCase):
    def test_password_hashing_and_comparing(self):
        password = "my-test-pass"
        hash = hash_password(password)
        self.assertTrue(hash is not password)
        self.assertTrue(is_password_equals(hash, password))


if __name__ == "__main__":
    unittest.main()
