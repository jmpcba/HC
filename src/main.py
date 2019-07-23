import errors
import logging
import json
from lib import pymysql
from service import DataBrokerService
from common import Tables, Chars

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context): 
    logger.info("HANDLER STARTING")
    logger.info(f"EVENT: {str(event)}")

    tables = event['queryStringParameters']['tables']
    tables = tables.upper().split(',')
    ret = ''
    
    try:
        validate_inputs(tables)
        f = DataBrokerService()
        ret = process_response(f.fetch(tables), 200)

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

def validate_inputs(tables):
    if not all(t in Tables.ALL_TABLES for t in tables):
        raise errors.InvalidParameter(tables)
