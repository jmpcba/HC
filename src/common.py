import os
import logging
from lib import pymysql

class Chars:
    EOL = '#'


class Tables:
    PRESTADORES ='PRESTADORES'
    PACIENTES = 'PACIENTES'
    MODULOS = 'MODULOS'
    SUB_MODULOS = 'SUBMODULOS'
    LIQUIDACIONES = 'LIQUIDACIONES'
    ALL_TABLES = [
                PRESTADORES,
                PACIENTES,
                MODULOS,
                SUB_MODULOS,
                LIQUIDACIONES,
                ]


class RDSConfig:
    RDS_HOST = "dev-database-1.c0rtb6x1vjcr.us-east-1.rds.amazonaws.com"
    NAME = 'admin'
    PWD = os.environ['db_password']
    DB = 'DESARROLLO'


class RDS:

    def __init__(self):
        self._db = RDSConfig.DB

    def open_connection(self):
        return pymysql.connect(RDSConfig.RDS_HOST, user=RDSConfig.NAME,
                                   passwd=RDSConfig.PWD, db=self._db, connect_timeout=5)

    def select_one(self, sql): 
            cnn = self.open_connection() 
            with cnn:
                cur = cnn.cursor(pymysql.cursors.DictCursor)
                cur.execute(sql)
                result = cur.fetchone()
                return result
    
    def select_many(self, sql):
        cnn = self.open_connection() 
        with cnn:
            cur = cnn.cursor(pymysql.cursors.DictCursor)
            cur.execute(sql)
            result = cur.fetchall()
            return result
    
    def insert(self, sql):
        cnn = self.open_connection()
            
        try:
            
            if not isinstance(sql, (list, tuple)):
                raise ValueError("must provide a list or tuple of SQL statements")
            
            with cnn:
                cur = cnn.cursor()
                
                for s in sql:
                    cur.execute(s)
                
                cnn.commit
        
        except Exception as e:
            cnn.rollback()
            logging.warning(e)


def convert_to_dict(obj):
  """
  A function takes in a custom object and returns a dictionary representation of the object.
  This dict representation includes meta data such as the object's module and class names.
  """

  #  Populate the dictionary with object meta data
  obj_dict = {
      "__class__": obj.__class__.__name__,
      "__module__": obj.__module__
  }

  #  Populate the dictionary with object properties
  obj_dict.update(obj.__dict__)

  return obj_dict