import logging
from controllers import Controller


class Service:
    @staticmethod
    def execute(resource, http_method, query_string, body):
        controller = Controller.factory(resource)
        http_method = http_method.upper()
        if not query_string:
            query_string = {}

        logging.info(f'RESOURCE: {resource}')
        logging.info(f'HTTP METHOD: {http_method}')
        logging.info(f'QUERY STRING: {query_string}')
        logging.info(f'BODY: {body}')

        if http_method == 'GET':
            controller.read(**query_string)
        elif http_method == 'POST':
            controller.create(body, **query_string)
        elif http_method == 'PUT':
            controller.update(body, **query_string)
        elif http_method == 'DELETE':
            controller.delete()

        logging.info(f'RESPONSE: {controller.response.http_response}')
        return controller.response.http_response
