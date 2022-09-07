"""File contains working models"""


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
