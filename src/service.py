import json
import errors
from lib import pymysql
import logging
from common import RDS, Tables

class DataBrokerService:

    def fetch(self, table, object_id=None):
        
        sql = ''
        rds = RDS()
        logging.info("Fetching from DB")
        if object_id:
            sql= 'SELECT * FROM %s WHERE id=%s' % (table, object_id)
            result = rds.select_one(sql)
        else:
            sql = 'SELECT * FROM %s' %(table,)
            result = rds.select_many(sql)
        
        if result:
            return result
        else:
            raise errors.ObjectNotFoundError(object_id)