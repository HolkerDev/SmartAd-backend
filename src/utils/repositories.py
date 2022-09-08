"""Module that contains user repository related code"""
from typing import Optional
from mypy_boto3_dynamodb.service_resource import Table
from src.utils.models import FullUser, User


class UserRepository:
    """Repository for managing users"""

    def __init__(self, table: Table) -> None:
        self.client: Table = table

    def find_by_email(self, email: str) -> Optional[User]:
        """Finds a user entity using [email]. Returns None if there is no user with this email"""
        result = self.client.get_item(Key={"pk": f"user#{email}", "sk": "none"})
        if not result or "Item" not in result:
            return None
        item: dict = result["Item"]
        return User.from_item(item)

    def find_by_email_f(self, email: str) -> Optional[FullUser]:
        """Finds a [FullUser] using [email]. Returns None if there is no user with this email"""
        result = self.client.get_item(Key={"pk": f"user#{email}", "sk": "none"})
        if not result or "Item" not in result:
            return None
        item: dict = result["Item"]
        return FullUser.from_item(item)

    def create(self, email: str, password: bytes):
        """Creates a user using [email] and [password] fields"""
        self.client.put_item(
            Item={
                "pk": f"user#{email}",
                "sk": "none",
                "email": email,
                "password": password,
            }
        )
