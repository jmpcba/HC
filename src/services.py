import json
import errors
import logging
import pymysql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from common import to_dict
from models import Base, Prestador,Paciente, Modulo, SubModulo, Zona, RDSConfig
from errors import ObjectNotFoundError

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
    def __init__(self):
        self.response = Response()

class DataBrokerService(Service):
    
    def get(self, in_tables):
        
        result = {}
        
        try:
            for t in RDSConfig.TABLES:
                if t['table_name'] in in_tables:
                    logging.info(f"Fetching table {t['table_name']}")
                    result[t['table_name']] = [vars(r) for r in session.query(t['model']).all()]
            if result:
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


class PrestadoresService(Service):
    # INSERT
    def post(self, new_prestador):
        try:
            prestador = Prestador(CUIT=new_prestador['CUIT'], 
                                nombre=new_prestador['nombre'],
                                apellido=new_prestador['apellido'],
                                mail=new_prestador['mail'],
                                especialidad=new_prestador['especialidad'],
                                servicio=new_prestador['servicio'],
                                localidad=new_prestador['localidad'],
                                monto_feriado=new_prestador['monto_feriado'],
                                monto_semana=new_prestador['monto_semana'],
                                monto_fijo=new_prestador['monto_fijo'],
                                zona=new_prestador['zona'],
                                comentario=new_prestador['comentario'],
                                baja=new_prestador['baja']
                                )

            session.add(prestador)
            session.commit()
            self.response.code = 200
            self.response.body = f"New Prestador: {prestador.id} inserted"
        
        except KeyError as e:
            self.response.code = 403
            self.response.body = e
        
        except IntegrityError as e:
            self.response.code = 403
            self.response.body = e
        
        finally:
            if self.response.code != 200:
                logging.warning(f"ERROR: {str(self.response.body)}")

    
    # UPDATE
    def put(self, prest_mod):
        try:
            logging.info(f'Modifiying Prestador {1}')
            id = prest_mod['id']
            prestador = session.query(Prestador).filter(Prestador.id == id).first()

            prestador.CUIT=prest_mod['CUIT']
            prestador.nombre=prest_mod['nombre']
            prestador.apellido=prest_mod['apellido']
            prestador.mail=prest_mod['mail']
            prestador.especialidad=prest_mod['especialidad']
            prestador.servicio=prest_mod['servicio']
            prestador.localidad=prest_mod['localidad']
            prestador.monto_feriado=prest_mod['monto_feriado']
            prestador.monto_semana=prest_mod['monto_semana']
            prestador.monto_fijo=prest_mod['monto_fijo']
            prestador.zona=prest_mod['zona']
            prestador.comentario=prest_mod['comentario']
            prestador.baja=prest_mod['baja']

            session.commit()

            self.response.code = 200
            self.response.body = f"Prestador: {prestador.id} modified"
        
        except KeyError as e:
            self.response.code = 403
            self.response.body = f"Invalid Parameter: {e}"
        
        except IntegrityError as e:
            self.response.code = 403
            self.response.body = e
        
        finally:
            if self.response.code != 200:
                logging.warning(f"ERROR: {str(self.response.body)}")

    
    def delete(self):
        pass
    
    def get(self, id=None):
        try:
            if id:
                prestador = session.query(Prestador).filter(Prestador.id == id).first()
                if prestador:
                    self.response.code = 200
                    self.response.body = vars(prestador)
                else:
                    raise ObjectNotFoundError
            else:
                ds = DataBrokerService()
                ds.get(RDSConfig.PRESTADORES)
                self.response.code = ds.response.code
                self.response.body = ds.response.body['PRESTADORES']
                
        
        except ObjectNotFoundError as e:
            self.response.code = 404
            self.response.body = e
        
        except IntegrityError as e:
            self.response.code = 403
            self.response.body = e
        
        finally:
            if self.response.code != 200:
                logging.warning(f"ERROR: {str(self.response.body)}")
        
