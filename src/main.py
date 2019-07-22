import errors
import logging
import json
from lib import pymysql
from service import DataBrokerService
from common import Tables, Chars

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context): 
    logger.info(f"{Chars.EOL}\nHandler started")
    logger.info(f"EVENT: {str(event)}")
    logger.info(f"CONTEXT: {str(context)}")
    logger.info(Chars.EOL)

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
        logger.warning(f"ERROR: {str(e)}")
        ret = process_response(str(e), 404)
    except pymysql.MySQLError as e:
        logger.warning(f"ERROR: {str(e)}")
        ret = process_response(str(e), 500)
    except errors.InvalidParameter as e:
        logger.warning(f"ERROR: {str(e)}")
        ret = process_response(str(e), 400)
    except Exception as e:
        logger.warning(f"ERROR: {str(e)}")
        ret = process_response(str(e), 503)
    logging.info(f"RETURNING: {ret}")
    return ret

def process_response(response, status_code):
    return {
        'statusCode': status_code,
        'body': json.dumps(response, default=str)
        }

def validate_inputs(**kwargs):
    
    # check if id is int
    if kwargs['object_id']:
        if not isinstance(kwargs['object_id'], int):
            raise errors.InvalidParameter(kwargs)
    
    if kwargs['table'] not in Tables.ALL_TABLES:
        raise errors.InvalidParameter(kwargs)
