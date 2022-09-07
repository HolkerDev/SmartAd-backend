"""Utils which are helping to work with AWS raw objects"""
import json


class AwsResponse:
    """Class that implements an ApiGateway response abstraction"""

    status_code: int = 404
    body: dict = {}

    def __init__(self, status_code: int, body: dict) -> None:
        self.status_code = status_code
        self.body = body

    def build(self) -> dict:
        """Builds response, so AwsLambda can parse it"""
        return {"statusCode": self.status_code, "body": json.dumps(self.body)}


class AwsRequest:
    """Class that implements an ApiGateway event abstraction"""

    body: dict = {}
    headers: dict = {}
    path: dict = {}
    query: dict = {}

    def __init__(self, event: dict) -> None:
        if "body" in event and event["body"] is not None:
            self.body = json.loads(event["body"])
        if "headers" in event:
            self.headers = event["headers"]
        if "pathParameters" in event:
            self.path = event["pathParameters"]
        if "queryStringParameters" in event:
            self.query = event["queryStringParameters"]
