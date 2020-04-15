import json
import errors
import logging
import pymysql
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from models import Base, RDSConfig, Resources, RDSModel


engine = create_engine(RDSConfig.ENGINE)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class Response:
    """
    Response class. all Service Classes have a response object with a response code and a message
    """
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

    def __init__(self, resource):
            self.response = Response()
            self.resource = resource
            
            if resource == Resources.MODULO.value:
                self.model = RDSModel(resource)

    def get(self):
        
        result = None
        try:
            logging.info(f"Fetching table {self.model.table_name}")
            result = [vars(r) for r in session.query(self.model.model_map).all()]
            if result:
                self.response.body = result
            else:
                self.response.body = e
                self.response.code = 404
            
        except pymysql.MySQLError as e:
            self.response.body = e
            self.response.code = 500
            
        except Exception as e:
            self.response.body = e
            self.response.code = 503
        
        finally:
            if self.response.code != 200:
                logging.error(f"ERROR: {str(self.response.body)}")
    
    def post(self, body):
        try:
            logging.info(f"received request to insert new object in: {self.model.table_name}")
            logging.info(f'OBJECT: {json.dumps(body)}')
    
            new_object = self.model.model_map
            new_object = new_object(**body)
            
            session.add(new_object)
            session.commit()
            logging.info(f"New object inserted into DB: {self.model.table_name}")
            self.response.body = f'Nuevo objeto insertado en {self.model.table_name}'
        
        except KeyError as e:
            self.response.code = 500
            self.response.body = e
            session.rollback()
        
        except (IntegrityError) as e:
            session.rollback()
            self.response.code = 500
            self.response.body = 'El objeto ya existe'
        
        finally:
            if self.response.code != 200:
                logging.error(f"ERROR: {str(self.response.body)}")


    def put(self, body):
        try:
            logging.info(f'Modifiying table {self.model.table_name}')
            
            id = body['id']
            current = session.query(self.model.model_map).filter(self.model.model_map.id == id).first()

            new_object = self.model.model_map
            new_object = new_object(**body)


            if self.resource == Resources.MODULO.value:
                current.codigo = new_object.codigo
                current.medico = new_object.medico
                current.enfermeria = new_object.enfermeria
                current.kinesiologia = new_object.kinesiologia
                current.fonoaudiologia = new_object.fonoaudiologia
                current.cuidador = new_object.cuidador
                current.nutricion = new_object.nutricion
                current.ultima_modificacion = datetime.now()
                current.usuario_ultima_modificacion = new_object.usuario_ultima_modificacion

            session.commit()
            self.response.body = f'Objeto {self.model.table_name} modificado'
        
        except KeyError as e:
            self.response.code = 500
            self.response.body = f"Invalid Parameter: {e}"
            session.rollback()
        
        except IntegrityError as e:
            self.response.code = 500
            self.response.body = e
            session.rollback()
        
        finally:
            if self.response.code != 200:
                logging.error(f"ERROR: {str(self.response.body)}")
class AdminService:

    def __init__(self):
        self.response = Response()
        
    def post(self, body):
        logging.info(f'post method body: {body}')
        try:
            if body['operation'] == 'create':
                logging.info('Create tables operation')
                if not database_exists(engine.url):
                    logging.info('DB must be created')
                    create_database(engine.url)
                    logging.info('DB created')
                
                logging.info('creating tables')
                Base.metadata.create_all(engine)
                self.response.body = 'db create operation finished'
            
            if body['operation'] == 'drop':
                logging.info("dropping table usuarios")
                drop_database(engine.url)
                self.response.body = 'table usuarios dropped'

        except Exception as e:
            self.response.code = 500
            self.response.body = e
        
        finally:
            if self.response.code != 200:
                logging.error(f"ERROR: {str(self.response.body)}")
    
    def get(self):
        self.response.body = "Service is working"
