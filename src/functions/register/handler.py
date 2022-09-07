"""Registration handler logic"""
from json import JSONDecodeError
import logging as log
import os
import hashlib
from typing import Optional
import boto3
import jwt

from mypy_boto3_dynamodb import DynamoDBServiceResource
from mypy_boto3_dynamodb.service_resource import Table
from src.utils.aws_request import AwsRequest, AwsResponse


from src.utils.repositories import UserRepository

db: DynamoDBServiceResource = boto3.resource("dynamodb")  # type: ignore
table: Table = db.Table("smartad")
user_repository = UserRepository(table=table)


def handle(event: dict, _) -> dict:
    """Registration handler entrypoint"""
    try:
        request = AwsRequest(event)
    except JSONDecodeError as err:
        log.error("Error during parsing registration body: %s", err)
        return AwsResponse(400, {"error": "Wrong JSON body"}).build()
    return register(request=request).build()


def register(request: AwsRequest) -> AwsResponse:
    """Registration handler logic"""
    log.info("Handling registration endpoint...")
    email: Optional[str] = request.body.get("email")
    password: Optional[str] = request.body.get("password")

    if email is None or password is None:
        log.error("Missing fields in request body")
        return AwsResponse(400, {"error": "No email or password"})

    user = user_repository.find_by_email(email=email)
    if user:
        log.error("Found existing user with provided email")
        return AwsResponse(409, {"error": f"User with email {email} already exists"})

    encrypted_password = hash_password(password)

    user_repository.create(email, encrypted_password)

    # TODO: replace with env variable
    encoded_jwt: str = jwt.encode(payload={"email": email}, key="test-secret")

    return AwsResponse(200, {"token": encoded_jwt})


def hash_password(password: str) -> bytes:
    """Password encryption method"""
    salt: bytes = os.urandom(32)
    hashed_password: bytes = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000,
    )
    return salt + hashed_password


def is_password_equals(old_password: bytes, password_to_check: str) -> bool:
    """Method checks if provided password is the same with old one"""
    salt: bytes = old_password[:32]
    old_key: bytes = old_password[32:]
    new_key: bytes = hashlib.pbkdf2_hmac(
        "sha256",
        password_to_check.encode("utf-8"),
        salt,
        100000,
    )
    return new_key == old_key
