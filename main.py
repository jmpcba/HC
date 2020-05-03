import logging
import json
from service import Service

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(f'REQUEST\n{event}')

    method = event['httpMethod'].upper()
    body = event['body']
    query_string = event['queryStringParameters']

    try:
        logging.error(f"decoding request body to dict")
        body = json.loads(body)
    except (json.JSONDecodeError, TypeError) as e:
        logging.error(f"ERROR: skiping json decoding: {e}")

    resource = event['resource'].upper()
    resource = resource[resource.rfind('/')+1:]

    service_response = Service.execute(resource, method, query_string, body)
    logger.info(f'RESPONSE\n{service_response}')
    return service_response


"""
{
    "resource": "Resource path",
    "path": "Path parameter",
    "httpMethod": "Incoming request's method name"
    "headers": {String containing incoming request headers}
    "multiValueHeaders": {List of strings containing incoming request headers}
    "queryStringParameters": {query string parameters }
    "multiValueQueryStringParameters": {List of query string parameters}
    "pathParameters":  {path parameters}
    "stageVariables": {Applicable stage variables}
    "requestContext": {Request context, including authorizer-returned key-value pairs}
    "body": "A JSON string of the request payload."
    "isBase64Encoded": "A boolean flag to indicate if the applicable request payload is Base64-encode"
}
"""
