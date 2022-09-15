from json import JSONDecodeError
import logging
import boto3
from mypy_boto3_dynamodb import DynamoDBServiceResource
from mypy_boto3_dynamodb.service_resource import Table

from src.utils.aws_request import AwsRequest, AwsResponse
from src.utils.repositories import CategoryRepository


db: DynamoDBServiceResource = boto3.resource("dynamodb")  # type: ignore
table: Table = db.Table("smartad")
category_repository = CategoryRepository(table=table)


def handle(event: dict, _) -> dict:
    """Category handler entrypoint"""
    try:
        request = AwsRequest(event)
    except JSONDecodeError as err:
        logging.error("Error during parsing registration body: %s", err)
        return AwsResponse(400, {"error": "Wrong JSON body"}).build()
    return categories(request=request).build()


def categories(request: AwsRequest) -> AwsResponse:
    categories = category_repository.find_all()
    return AwsResponse(200, {"categories": categories})
