import errors
import logging
import json
from services import DataBrokerService, PrestadoresService, PacientesService

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def databroker_handler(event, context): 
    logger.info("DATA SERVICE HANDLER STARTING")
    logger.info(f"EVENT: {str(event)}")

    tables = event['queryStringParameters']['tables']
    tables = tables.upper().split(',')
    
    service = DataBrokerService()
    service.get(tables)
    return service.response.service_response


def prestador_handler(event, contex):
    
    logger.info(f'REQUEST\n{event}')
    
    service = PrestadoresService()

    if event['httpMethod'] == 'POST':
        
        body = event['body']
        service.post(json.loads(body))
    
    if event['httpMethod'] == 'PUT':
        body = event['body']
        service.put(json.loads(body))
    
    if event['httpMethod'] == 'GET':
        service.get()

    logger.info(f'RESPONSE\n{service.response.service_response}')
    return service.response.service_response


def paciente_handler(event, contex):
    
    logger.info(f'REQUEST\n{event}')
    
    service = PacientesService()

    if event['httpMethod'] == 'POST':
        
        body = event['body']
        service.post(json.loads(body))
    
    if event['httpMethod'] == 'PUT':
        body = event['body']
        service.put(json.loads(body))
    
    if event['httpMethod'] == 'GET':
        service.get()

    logger.info(f'RESPONSE\n{service.response.service_response}')
    return service.response.service_response

def resource_fabric(resource_name):
    

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
