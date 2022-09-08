import unittest

from src.utils.models import User


class ModelsTestModule(unittest.TestCase):
    def test_from_item_user_creation(self):
        email = "mytest@test.com"
        user = User.from_item({"email": email})
        self.assertIsNotNone(user)
        if user is not None:
            self.assertEqual(user.email, email)

    def test_from_item_user_creation_with_none(self):
        user = User.from_item({})
        self.assertIsNone(user)


if __name__ == "__main__":
    unittest.main()
