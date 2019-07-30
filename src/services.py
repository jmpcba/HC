import json
import errors
import logging
from lib import pymysql
from common import RDS, Tables


class Response:
    def __init__(self):
        self._code = 200
        self._body = 'EMPTY RESPONSE'
    
    @property
    def code(self):
        return self._code
    
    @code.setter
    def code(self, c):
        self._code = c
    
    @property
    def body(self):
        return self._body
    
    @body.setter
    def body(self, b):
        self._body = b
    
    @property
    def service_response(self):
        return self._parse_response()
    
    def _parse_response(self):
        return {
            'statusCode': self._code,
            'body': json.dumps(self._body, default=str)
            }

class Service:
    def __init__(self):
        self.response = Response()

class DataBrokerService(Service):
    
    def fetch_tables(self, tables):
        
        sql = ''
        rds = RDS()
        result = {}
        
        try:
            if not all(t in Tables.ALL_TABLES for t in tables):
                raise errors.InvalidParameter(tables)
            
            for t in tables:
                sql = 'SELECT * FROM %s' %(t,)
                logging.info(f"EXECUTING SQL: {sql}")
                result[t] = rds.select_many(sql)
            
            if result:
                logging.info(f'Returning {len(result)} entries')
                self.response.body = result
                self.response.code = 200
            else:
                raise errors.ObjectNotFoundError()
        
        except errors.ObjectNotFoundError as e:
            self.response.body = e
            self.response.code = 404
            
        except pymysql.MySQLError as e:
            self.response.body = e
            self.response.code = 500
        
        except errors.InvalidParameter as e:
            self.response.body = e
            self.response.code = 400
            
        except Exception as e:
            self.response.body = e
            self.response.code = 503
        
        finally:
            if self.response.code != 200:
                logging.warning(f"ERROR: {str(self.response.body)}")
            


class PrestadoresService:
    
    def __init__(self, id):
        self.id = id

    def add_new(self, **kwargs):
        required = ['CUIT', 'NOMBRE']
        if not all(r in kwargs.keys() for r in required):
            raise ValueError(f"Parameters are not valid. Required fields: {str(required)}")
        else:
            cuit = kwargs['CUIT']
            if cuit[-2:-1] != '-' or cuit[2:3] != '-':
                raise ValueError(f"CUIT Format is not valid")
        
        sql = []
        sql.append(f'INSERT INTO DESARROLLO.PRESTADORES (CUIT, NOMBRE) VALUES ("{kwargs["CUIT"]}", "{kwargs["NOMBRE"]}")')
        logging.info(f"INSERTED NEW PRESTADOR: {kwargs}")
        rds = RDS()
        rds.statement(sql)
    
    def update(self):
        pass
    
    def delete(self):
        pass
    
    def get_liquidacion(self):
        pass
