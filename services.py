import json
import logging
import pymysql
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy import create_engine, between
from sqlalchemy_utils import database_exists, create_database, drop_database
from RDS import Base, RDSConfig, Resources, RDSModel, Feriado


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
        self.model = RDSModel(resource)

    def get(self, **kwargs):
        year = kwargs.get('year')
        try:
            logging.info(f"Fetching table {self.model.table_name}")

            if self.resource == Resources.FERIADO and year:
                logging.info(f'Fetching feriados for year {year}')
                result = session.query(Feriado).filter(
                    between(Feriado.fecha, f'1/1/{year}', f'12/31/{year}'))
            else:
                result = [vars(r) for r in session.query(self.model.model_map).all()]

            if result:
                # remove _sa_instance_state before returning the object
                [r.pop('_sa_instance_state', None) for r in result]
                self.response.body = result
            else:
                self.response.body = f'No se encontro la tabla {self.model.table_name}'
                self.response.code = 404
            
        except pymysql.MySQLError as e:
            logging.error(e)
            self.response.body = e
            self.response.code = 500
            
        except Exception as e:
            logging.error(e)
            self.response.body = e
            self.response.code = 503
    
    def post(self, body):
        try:
            logging.info(f"received request to insert new object in: {self.model.table_name}")
            logging.info(f'OBJECT: {json.dumps(body)}')
            new_object = self.model.model_map

            if self.resource == Resources.PRACTICA and type(body) == list:
                logging.info(f"Inserting list of practicas")
                error_list = []
                errors = False
                for practica in body:
                    try:
                        new_object = new_object(**practica)
                        session.add(new_object)
                        session.commit()
                    except Exception as e:
                        logging.error(e)
                        error_list.append({'fecha': new_object.fecha, 'error': e})
                        errors = True

                if errors:
                    self.response.code = 500
                    self.response.body = error_list

            else:
                new_object = new_object(**body)
                session.add(new_object)
                session.commit()
            logging.info(f"New object inserted into DB: {self.model.table_name}")
            self.response.body = f'Nuevo objeto insertado en {self.model.table_name}'
        
        except KeyError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e
            session.rollback()
        
        except IntegrityError as e:
            logging.error(e)
            session.rollback()
            self.response.code = 500
            self.response.body = 'El objeto ya existe'

    def put(self, body):
        try:
            logging.info(f'Modifiying table {self.model.table_name}')
            
            new_object = self.model.model_map
            new_object = new_object(**body)
            current = session.query(self.model.model_map).filter(self.model.model_map.id == new_object.id).first()
            
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
            
            elif self.resource == Resources.SUBMODULO.value:
                current.codigo = new_object.codigo
                current.descripcion = new_object.descripcion
                current.ultima_modificacion = datetime.now()
                current.usuario_ultima_modificacion = new_object.usuario_ultima_modificacion
            
            elif self.resource == Resources.PRESTADOR.value:
                current.CUIT = new_object.CUIT
                current.nombre = new_object.nombre
                current.apellido = new_object.apellido
                current.mail = new_object.mail
                current.especialidad = new_object.especialidad
                current.servicio = new_object.servicio
                current.localidad = new_object.localidad
                current.monto_feriado = new_object.monto_feriado
                current.monto_semana = new_object.monto_semana
                current.monto_fijo = new_object.monto_fijo
                current.monto_diferencial = new_object.monto_diferencial
                current.zona = new_object.zona
                current.comentario = new_object.comentario
                current.baja = new_object.baja
                current.ultima_modificacion = datetime.now()
                current.usuario_ultima_modificacion = new_object.usuario_ultima_modificacion
            
            elif self.resource == Resources.PACIENTE.value:
                current.afiliado = new_object.afiliado
                current.DNI = new_object.DNI
                current.nombre = new_object.nombre
                current.apellido = new_object.apellido
                current.localidad = new_object.localidad
                current.obra_social = new_object.obra_social
                current.observacion = new_object.observacion
                current.modulo = new_object.modulo
                current.ultima_modificacion = datetime.now()
                current.usuario_ultima_modificacion = new_object.usuario_ultima_modificacion
            
            elif self.resource == Resources.PRACTICA.value:
                current.cuit = new_object.cuit
                current.afiliado = new_object.afiliado
                current.modulo = new_object.modulo
                current.sub_modulo = new_object.sub_modulo
                current.id_prest = new_object.id_prest
                current.hs_normales = new_object.hs_normales
                current.hs_feriados = new_object.hs_feriados
                current.hs_diferencial = new_object.hs_diferencial
                current.fecha = new_object.fecha
                current.observaciones = new_object.observaciones
                current.observaciones_paciente = new_object.observaciones_paciente
                current.observaciones_prestacion = new_object.observaciones_prestacion
                current.ultima_modificacion = datetime.now()
                current.usuario_ultima_modificacion = new_object.usuario_ultima_modificacion
            
            elif self.resource == Resources.ZONA.value:
                current.nombre = new_object.nombre
                current.mail = new_object.mail
                current.pwd = new_object.pwd
                current.propietario = new_object.propietario
                current.ultima_modificacion = datetime.now()
                current.usuario_ultima_modificacion = new_object.usuario_ultima_modificacion
            
            elif self.resource == Resources.LIQUIDACION.value:
                current.cuit = new_object.cuit
                current.localidad = new_object.localidad
                current.especialidad = new_object.especialidad
                current.mes = new_object.mes
                current.id_prest = new_object.id_prest
                current.hs_normales = new_object.hs_normales
                current.hs_feriados = new_object.hs_feriados
                current.hs_diferencial = new_object.hs_diferencial
                current.importe_normal = new_object.importe_normal
                current.importe_feriado = new_object.importe_feriado
                current.importe_diferencial = new_object.importe_diferencial
                current.monto_fijo = new_object.monto_fijo
                current.ultima_modificacion = datetime.now()
                current.usuario_ultima_modificacion = new_object.usuario_ultima_modificacion
            
            elif self.resource == Resources.FERIADO.value:
                current.fecha = new_object.fecha
                current.descripcion = new_object.descripcion
                current.ultima_modificacion = datetime.now()
                current.usuario_ultima_modificacion = new_object.usuario_ultima_modificacion
            
            elif self.resource == Resources.ESPECIALIDAD.value:
                current.nombre = new_object.nombre

            else:
                raise Exception(f"el recurso {self.resource} es invalido")

            session.commit()
            self.response.body = f'Objeto {current.id} modificado'
        
        except KeyError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = f"Invalid Parameter: {e}"
            session.rollback()
        
        except IntegrityError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = 'Objecto duplicado'
            session.rollback()

    def delete(self, body):
        try:
            logging.info(f"received request to delete new object in: {self.model.table_name}")
            logging.info(f'OBJECT: {json.dumps(body)}')

            del_object = self.model.model_map
            del_object = del_object(**body)

            current = session.query(self.model.model_map).filter(self.model.model_map.id == del_object.id).first()
            session.delete(current)
            session.commit()
            logging.info(f"object: {self.model.table_name} deleted from DB")
            self.response.body = f'Object deleted from table: {self.model.table_name}'

        except KeyError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e
            session.rollback()

        except IntegrityError as e:
            logging.error(e)
            session.rollback()
            self.response.code = 500
            self.response.body = 'El objeto ya existe'

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
            logging.error(e)
            self.response.code = 500
            self.response.body = e
    
    def get(self):
        self.response.body = "Service is working"
