import logging
import json
from .services import Service, AdminService
from .RDS import Resources

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# TODO notas: los recursos basicos como prestadores, zonas tienen que devolver
# la tabla completa con GET, actualizar agregar y eliminar
# practicas es el unico que va a filtrar.
# liquidaciones TBD
# hay un solo main, tengo que averiguar recurso y metodo

def handler(event, context):
    logger.info(f'REQUEST\n{event}')

    method = event['httpMethod'].upper()
    body = event['body']

    try:
        body = json.loads(body)
    except (json.JSONDecodeError, TypeError) as e:
        logging.error(f"ERROR: skiping json decoding: {e}")

    resource = event['resource'].upper()
    resource = resource[resource.rfind('/')+1:]

    service = Service(resource)

    if resource == Resources.ADMIN:
        service = AdminService()

    if method == 'POST':
        service.post(body)

    elif method == 'PUT':
        service.put(body)

    elif method == 'GET':
        service.get()

    logger.info(f'RESPONSE\n{service.response.service_response}')
    return service.response.service_response

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
