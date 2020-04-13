import json
import errors
import logging
import pymysql
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
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
                logging.error(f"ERROR: {str(self.response.body)}")


class PrestadoresService(Service):
    # INSERT
    def post(self, new_prestador):
        try:
            logging.info("received request to insert new prestador")
            logging.info(json.dumps(new_prestador))
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
                                baja=new_prestador['baja'],
                                ultima_modificacion=datetime.now(),
                                usuario_ultima_modificacion=new_prestador['usuario_ultima_modificacion']
                                )

            session.add(prestador)
            session.commit()
            logging.info("New prestador inserted into DB")
            self.response.body = f"New Prestador: {prestador.id} inserted"
        
        except KeyError as e:
            self.response.code = 500
            self.response.body = e
            session.rollback()
        
        except (IntegrityError, StatementError) as e:
            session.rollback()
            self.response.code = 500
            self.response.body = e
        
        finally:
            if self.response.code != 200:
                logging.error(f"ERROR: {str(self.response.body)}")

    
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
            prestador.baja=prest_mod['baja'],
            prestador.usuario_ultima_modificacion=new_mod['usuario'],
            prestador.ultima_modificacion=datetime.now()

            session.commit()

            self.response.body = f"Prestador: {prestador.id} modified"
        
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

    
    def delete(self):
        pass
    
    def get(self, id=None):
        try:
            if id:
                prestador = session.query(Prestador).filter(Prestador.id == id).first()
                if prestador:
                    self.response.body = vars(prestador)
                else:
                    raise ObjectNotFoundError
            else:
                ds = DataBrokerService()
                ds.get(RDSConfig.PRESTADORES)
                self.response.code = ds.response.code
                self.response.body = ds.response.body[RDSConfig.PRESTADORES]
                
        
        except ObjectNotFoundError as e:
            self.response.code = 404
            self.response.body = e
        
        except IntegrityError as e:
            self.response.code = 500
            self.response.body = e
        
        finally:
            if self.response.code != 200:
                logging.error(f"ERROR: {str(self.response.body)}")

class PacientesService(Service):
    # INSERT
    def post(self, new_paciente):
        try:
            paciente = Paciente(afiliado=new_paciente['afiliado'], 
                                DNI=new_paciente['DNI'], 
                                nombre=new_paciente['nombre'],
                                apellido=new_paciente['apellido'],
                                localidad=new_paciente['localidad'],
                                obra_social=new_paciente['obra_social'],
                                observacion=new_paciente['observacion'],
                                modulo=new_paciente['modulo'],
                                sub_modulo=new_paciente['sub_modulo'],
                                baja=new_paciente['baja'],
                                ultima_modificacion = datetime.now(),
                                usuario_ultima_modificacion=new_prestador['usuario_ultima_modificacion']
                                )

            session.add(paciente)
            session.commit()
            self.response.body = f"New Paciente: {paciente.afiliado} inserted"
        
        except KeyError as e:
            self.response.code = 500
            self.response.body = e
            session.rollback()
        
        except (IntegrityError, StatementError) as e:
            session.rollback()
            self.response.code = 500
            self.response.body = e
        
        finally:
            if self.response.code != 200:
                logging.error(f"ERROR: {str(self.response.body)}")

    
    # UPDATE
    def put(self, pac_mod):
        try:
            
            afiliado = pac_mod['afiliado']
            logging.info(f'Modifiying Paciente {afiliado}')
            paciente = session.query(Paciente).filter(Paciente.afiliado == afiliado).first()

            paciente.DNI=pac_mod['DNI']
            paciente.nombre=pac_mod['nombre']
            paciente.apellido=pac_mod['apellido']
            paciente.localidad=pac_mod['localidad']
            paciente.obra_social=pac_mod['obra_social']
            paciente.observacion=pac_mod['observacion']
            paciente.modulo=pac_mod['modulo']
            paciente.sub_modulo=pac_mod['sub_modulo']
            paciente.baja=pac_mod['baja']

            session.commit()

            self.response.body = f"Paciente: {paciente.afiliado} modified"
        
        except KeyError as e:
            self.response.code = 500
            self.response.body = f"Invalid Parameter: {e}"
        
        except IntegrityError as e:
            self.response.code = 500
            self.response.body = e
        
        finally:
            if self.response.code != 200:
                logging.error(f"ERROR: {str(self.response.body)}")

    
    def delete(self):
        pass
    
    def get(self, id=None):
        try:
            if id:
                paciente = session.query(Paciente).filter(Paciente.afiliado == id).first()
                if paciente:
                    self.response.body = vars(paciente)
                else:
                    raise ObjectNotFoundError
            else:
                ds = DataBrokerService()
                ds.get(RDSConfig.PACIENTES)
                self.response.code = ds.response.code
                self.response.body = ds.response.body[RDSConfig.PACIENTES]
                
        
        except ObjectNotFoundError as e:
            self.response.code = 404
            self.response.body = e
        
        except IntegrityError as e:
            self.response.code = 500
            self.response.body = e
        
        finally:
            if self.response.code != 200:
                logging.error(f"ERROR: {str(self.response.body)}")

        
class AdminService(Service):

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

        except Exception as e:
            self.response.code = 500
            self.response.body = e
        
        finally:
            if self.response.code != 200:
                logging.error(f"ERROR: {str(self.response.body)}")
    
    def get(self):
        self.response.body = "Service is working"
