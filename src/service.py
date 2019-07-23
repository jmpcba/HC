import json
import errors
import logging
from lib import pymysql
from common import RDS, Tables

class DataBrokerService:

    def fetch(self, tables):
        
        sql = ''
        rds = RDS()
        result = {}
        
        for t in tables:
            sql = 'SELECT * FROM %s' %(t,)
            logging.info(f"EXECUTING SQL: {sql}")
            result[t] = rds.select_many(sql)
        
        if result:
            return result
        else:
            raise errors.ObjectNotFoundError()
