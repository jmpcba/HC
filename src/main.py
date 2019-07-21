import errors
import logging
import json
from lib import pymysql
from service import DataBrokerService
from common import Tables, Chars


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def handler(event, context): 
    logging.info(f"{Chars.EOL}\nHandler started")
    logging.info(f"EVENT: {str(event)}")
    logging.info(f"CONTEXT: {str(context)}")
    logging.info(Chars.EOL)

    object_id = None
    if 'id' in event['queryStringParameters']:
        object_id = int(event['queryStringParameters']['id'])
    
    table = event['queryStringParameters']['table']
    ret = ''
    
    try:
        validate_inputs(object_id=object_id, table=table)
        f = DataBrokerService()
        ret = process_response(f.fetch(table, object_id), 200)

    except errors.ObjectNotFoundError as e:
        logging.warning(f"ERROR: {str(e)}")
        ret = process_response(str(e), 404)
    except pymysql.MySQLError as e:
        logging.warning(f"ERROR: {str(e)}")
        ret = process_response(str(e), 500)
    except errors.InvalidParameter as e:
        logging.warning(f"ERROR: {str(e)}")
        ret = process_response(str(e), 400)
    except Exception as e:
        logging.warning(f"ERROR: {str(e)}")
        ret = process_response(str(e), 503)
    
    return ret

def process_response(response, status_code):
    return {
        'statusCode': status_code,
        'body': json.dumps(response)
        }

def validate_inputs(**kwargs):
    
    # check if id is int
    if kwargs['object_id']:
        if not isinstance(kwargs['object_id'], int):
            raise errors.InvalidParameter(kwargs)
    
    if kwargs['table'] not in Tables.ALL_TABLES:
        raise errors.InvalidParameter(kwargs)
