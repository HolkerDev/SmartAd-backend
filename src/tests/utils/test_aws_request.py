import json
import unittest

from src.utils.aws_request import AwsRequest, AwsResponse


class AwsRequestsTestModule(unittest.TestCase):
    def test_aws_resposne_building(self):
        response = AwsResponse(200, {"message": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, {"message": "test"})

    def test_build_correct_raw_aws_response(self):
        status_code = 200
        body_obj = {"message": "test"}
        response = AwsResponse(status_code, body_obj)
        raw_response = response.build()
        self.assertEqual(raw_response["statusCode"], status_code)
        self.assertEqual(raw_response["body"], json.dumps(body_obj))

    def test_aws_request_empty_building(self):
        request = AwsRequest({})
        self.assertEqual(request.body, {})
        self.assertEqual(request.headers, {})
        self.assertEqual(request.path, {})
        self.assertEqual(request.query, {})

    def test_aws_request_building(self):
        body = {"message": "test"}
        headers = {"accept": "yep"}
        pathParams = {"one": 1}
        query = {"one": 2}
        request = AwsRequest(
            {
                "body": json.dumps(body),
                "headers": headers,
                "pathParameters": pathParams,
                "queryStringParameters": query,
            }
        )
        self.assertEqual(request.query, query)
        self.assertEqual(request.path, pathParams)
        self.assertEqual(request.body, body)
        self.assertEqual(request.headers, headers)

    def test_aws_request_building_with_empty_dicts(self):
        request = AwsRequest(
            {
                "body": None,
                "headers": {},
                "pathParameters": {},
                "queryStringParameters": {},
            }
        )
        self.assertEqual(request.body, {})
        self.assertEqual(request.headers, {})
        self.assertEqual(request.path, {})
        self.assertEqual(request.query, {})


if __name__ == "__main__":
    unittest.main()
