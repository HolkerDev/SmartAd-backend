from base64 import encode
import unittest
from unittest.mock import MagicMock
from mypy_boto3_dynamodb.service_resource import Table
from mypy_boto3_dynamodb.type_defs import (
    GetItemOutputTableTypeDef,
    ConsumedCapacityTableTypeDef,
    ResponseMetadataTypeDef,
)

from src.utils.repositories import UserRepository


class RepositoriesModuleTest(unittest.TestCase):
    def test_find_by_email_OK(self):
        table = MagicMock(Table)
        # TODO: Place it in a separate method
        consumed_capacity = MagicMock(ConsumedCapacityTableTypeDef)
        response_metadata = MagicMock(ResponseMetadataTypeDef)
        table.get_item.return_value = GetItemOutputTableTypeDef(
            Item={"email": "test@email!"},
            ConsumedCapacity=consumed_capacity,
            ResponseMetadata=response_metadata,
        )
        repo = UserRepository(table)
        user = repo.find_by_email("test@email!")
        if user is None:
            self.fail()
        else:
            self.assertEqual(user.email, "test@email!")

    def test_find_by_email_empty_response(self):
        table = MagicMock(Table)
        # TODO: Place it in a separate method
        consumed_capacity = MagicMock(ConsumedCapacityTableTypeDef)
        response_metadata = MagicMock(ResponseMetadataTypeDef)
        table.get_item.return_value = GetItemOutputTableTypeDef(
            Item={},
            ConsumedCapacity=consumed_capacity,
            ResponseMetadata=response_metadata,
        )
        repo = UserRepository(table)
        user = repo.find_by_email("test@email!")
        self.assertIsNone(user)

    def test_find_by_email_none_response(self):
        table = MagicMock(Table)
        table.get_item.return_value = None
        repo = UserRepository(table)
        user = repo.find_by_email("test@email!")
        self.assertIsNone(user)

    def test_create_with_provided_values(self):
        table = MagicMock(Table)
        repo = UserRepository(table)
        email = "email"
        password = "password".encode()
        repo.create(email, password)
        table.put_item.assert_called_with(
            Item={
                "pk": f"user#{email}",
                "sk": "none",
                "email": email,
                "password": password,
            }
        )


if __name__ == "__main__":
    unittest.main()
