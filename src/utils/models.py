"""File contains working models"""


from pkgutil import iter_modules
from time import time
from xmlrpc.client import boolean


class User:
    """User model"""

    def __init__(self, email: str) -> None:
        self.email = email

    @classmethod
    def from_item(cls, item: dict):
        """Creates a user domain object from dynamodb response"""
        if "email" not in item or item["email"] is None:
            return None
        return cls(item["email"])


class FullUser:
    """User model with secret fields"""

    def __init__(self, email: str, password: bytes) -> None:
        self.email = email
        self.password = password

    @classmethod
    def from_item(cls, item: dict):
        if not is_valid_full_user_item(item=item):
            return None
        return cls(item["email"], item["password"])


def is_valid_full_user_item(item: dict) -> boolean:
    if "email" not in item or "password" not in item:
        return False
    if item["email"] is None or item["password"] is None:
        return False
    return True
