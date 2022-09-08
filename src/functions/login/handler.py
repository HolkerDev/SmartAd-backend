from json import JSONDecodeError
import logging
import boto3
from typing import Optional

from src.utils.aws_request import AwsRequest, AwsResponse
from mypy_boto3_dynamodb import DynamoDBServiceResource
from mypy_boto3_dynamodb.service_resource import Table
from src.utils.jwt_session import generate_token
from src.utils.password import is_password_equals

from src.utils.repositories import UserRepository

db: DynamoDBServiceResource = boto3.resource("dynamodb")  # type: ignore
table: Table = db.Table("smartad")
user_repository = UserRepository(table=table)


def handle(event: dict, _) -> dict:
    """Registration handler entrypoint"""
    try:
        request = AwsRequest(event)
    except JSONDecodeError as err:
        logging.error("Error during parsing registration body: %s", err)
        return AwsResponse(400, {"error": "Wrong JSON body"}).build()
    return {}


def login(request: AwsRequest) -> AwsResponse:
    email: Optional[str] = request.body.get("email")
    password: Optional[str] = request.body.get("password")
    if email is None or password is None:
        logging.error("Wrong request body")
        return AwsResponse(400, {"error": "Wrong request body"})

    user = user_repository.find_by_email_f(email=email)
    if user is None or not is_password_equals(user.password, password):
        return AwsResponse(401, {"error": "Wrong credentials"})

    token = generate_token({"email": email})
    return AwsResponse(200, body={"token": token})
