import errors
import logging
import json
from lib import pymysql
from services import DataBrokerService
from common import Tables, Chars

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def databroker_handler(event, context): 
    logger.info("HANDLER STARTING")
    logger.info(f"EVENT: {str(event)}")

    tables = event['queryStringParameters']['tables']
    tables = tables.upper().split(',')
    
    service = DataBrokerService()
    service.get_tables(tables)
    return service.response.service_response

    