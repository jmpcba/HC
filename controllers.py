import logging
import json
import Entities
from datetime import datetime
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy import create_engine, between, and_
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError, StatementError
from pymysql import MySQLError
from Entities import Base
from config import RDSConfig

engine = create_engine(RDSConfig.ENGINE)
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class Controller:
    @staticmethod
    def factory(resource):
        if resource == "FERIADO":
            return ControllerFeriado()
        elif resource == 'MODULO':
            return ControllerModulo()
        elif resource == 'PACIENTE':
            return ControllerPaciente()
        elif resource == 'ZONA':
            return ControllerZona()
        elif resource == 'PRACTICA':
            return ControllerPractica()
        elif resource == 'PRESTADOR':
            return ControllerPrestador()
        elif resource == 'SUBMODULO':
            return ControllerSubModulo()
        elif resource == 'ADMIN':
            return ControllerAdmin()


class Response:
    """
    Response class. all Service Classes have a response object with a response code and a message
    """

    def __init__(self):
        self._code = 200
        self._body = ''

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
    def http_response(self):
        return {
            'statusCode': self._code,
            'body': json.dumps(self._body, default=str)
        }


class BaseController:
    def __init__(self):
        self.entityClass = None
        self.response = Response()

    def _parse_error(self, e):
        err_msg = e.args[0]
        ret_msg = ''
        if '1062' in err_msg:
            start_pos = err_msg.find('Duplicate entry') + 17
            key_pos = err_msg.find('for key') - 2
            end_pos = err_msg.rfind(')') - 2
            cod = err_msg[start_pos: key_pos]
            key = err_msg[key_pos + 11: end_pos]
            ret_msg = f'Ya existe {key}: {cod}'
        return ret_msg

    def create(self, body, **kwargs):
        logging.info(f"INSERTING: {json.dumps(body)}")
        new_object = self.entityClass(**body)

        try:
            with session_scope() as s:
                s.add(new_object)
                logging.info(f"object added into {new_object.table_name}")
                self.response.body = f'Objeto insertado en tabla {new_object.table_name}'
        except IntegrityError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = self._parse_error(e)

    def read(self, **kwargs):
        result = None
        obj_id = kwargs.get('id')

        try:
            with session_scope() as s:
                if obj_id:
                    logging.info(f"Fetching object with ID: {obj_id}")
                    result = [vars(r) for r in s.query(self.entityClass).filter(self.entityClass.id == obj_id).all()]
                else:
                    logging.info(f"Fetching table {self.entityClass.table_name}")
                    result = [vars(r) for r in s.query(self.entityClass).all()]

                if result:
                    # remove _sa_instance_state before returning the object
                    [r.pop('_sa_instance_state', None) for r in result]
                    self.response.body = result

        except MySQLError as e:
            logging.error(e)
            self.response.body = e
            self.response.code = 500

    def delete(self):
        pass


class ControllerZona(BaseController):
    def __init__(self):
        super().__init__()
        self.entityClass = Entities.Zona

    def update(self, body, **kwargs):
        try:
            logging.info(f'Modifiying table {self.entityClass.table_name}')
            new_zona = self.entityClass(**body)

            with session_scope() as s:
                current = s.query(self.entityClass).filter(self.entityClass.id == new_zona.id).first()
                current.nombre = new_zona.nombre
                current.mail = new_zona.mail
                current.pwd = new_zona.pwd
                current.propietario = new_zona.propietario
                current.ultima_modificacion = datetime.now()
                current.usuario_ultima_modificacion = new_zona.usuario_ultima_modificacion
                self.response.body = f'Objeto {current.id} modificado'

        except IntegrityError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e


class ControllerModulo(BaseController):
    def __init__(self):
        super().__init__()
        self.entityClass = Entities.Modulo

    def update(self, body, **kwargs):
        try:
            logging.info(f'Modifiying table {self.entityClass.table_name}')
            new_modulo = self.entityClass(**body)

            with session_scope() as s:
                current = s.query(self.entityClass).filter(self.entityClass.id == new_modulo.id).first()
                current.codigo = new_modulo.codigo
                current.medico = new_modulo.medico
                current.enfermeria = new_modulo.enfermeria
                current.kinesiologia = new_modulo.kinesiologia
                current.fonoaudiologia = new_modulo.fonoaudiologia
                current.cuidador = new_modulo.cuidador
                current.nutricion = new_modulo.nutricion
                current.ultima_modificacion = datetime.now()
                current.usuario_ultima_modificacion = new_modulo.usuario_ultima_modificacion
            self.response.body = f'Objeto {current.id} en {self.entityClass.table_name} modificado'

        except IntegrityError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e


class ControllerSubModulo(BaseController):
    def __init__(self):
        super().__init__()
        self.entityClass = Entities.SubModulo

    def update(self, body, **kwargs):
        try:
            logging.info(f'Modifiying table {self.entityClass.table_name}')
            new_sub_modulo = self.entityClass(**body)

            with session_scope() as s:
                current = s.query(self.entityClass).filter(self.entityClass.id == new_sub_modulo.id).first()
                current.codigo = new_sub_modulo.codigo
                current.descripcion = new_sub_modulo.descripcion
                current.ultima_modificacion = datetime.now()
                current.usuario_ultima_modificacion = new_sub_modulo.usuario_ultima_modificacion
            self.response.body = f'Objeto {current.id} en {self.entityClass.table_name} modificado'

        except IntegrityError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e


class ControllerPrestador(BaseController):
    def __init__(self):
        super().__init__()
        self.entityClass = Entities.Prestador

    def update(self, body, **kwargs):
        try:
            logging.info(f'Modifiying table {self.entityClass.table_name}')
            new_prestador = self.entityClass(**body)

            with session_scope() as s:
                current = s.query(self.entityClass).filter(self.entityClass.id == new_prestador.id).first()
                current.CUIT = new_prestador.CUIT
                current.nombre = new_prestador.nombre
                current.apellido = new_prestador.apellido
                current.mail = new_prestador.mail
                current.especialidad = new_prestador.especialidad
                current.servicio = new_prestador.servicio
                current.localidad = new_prestador.localidad
                current.monto_feriado = new_prestador.monto_feriado
                current.monto_semana = new_prestador.monto_semana
                current.monto_fijo = new_prestador.monto_fijo
                current.monto_diferencial = new_prestador.monto_diferencial
                current.zona = new_prestador.zona
                current.comentario = new_prestador.comentario
                current.baja = new_prestador.baja
                current.ultima_modificacion = datetime.now()
                current.usuario_ultima_modificacion = new_prestador.usuario_ultima_modificacion
            self.response.body = f'Objeto {current.id} en {self.entityClass.table_name} modificado'

        except IntegrityError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e


class ControllerPaciente(BaseController):
    def __init__(self):
        super().__init__()
        self.entityClass = Entities.Paciente

    def update(self, body, **kwargs):
        try:
            logging.info(f'Modifiying table {self.entityClass.table_name}')
            new_paciente = self.entityClass(**body)

            with session_scope() as s:
                current = s.query(self.entityClass).filter(self.entityClass.id == new_paciente.id).first()
                current.afiliado = new_paciente.afiliado
                current.DNI = new_paciente.DNI
                current.nombre = new_paciente.nombre
                current.apellido = new_paciente.apellido
                current.localidad = new_paciente.localidad
                current.obra_social = new_paciente.obra_social
                current.observacion = new_paciente.observacion
                current.modulo = new_paciente.modulo
                current.ultima_modificacion = datetime.now()
                current.usuario_ultima_modificacion = new_paciente.usuario_ultima_modificacion
            self.response.body = f'Objeto {current.id} en {self.entityClass.table_name} modificado'

        except IntegrityError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e


class ControllerFeriado(BaseController):
    def __init__(self):
        super().__init__()
        self.entityClass = Entities.Feriado

    def read(self, **kwargs):
        year = kwargs.get('year')

        if year:
            with session_scope() as s:
                result = [vars(r) for r in s.query(self.entityClass).filter(self.entityClass.fecha.between(
                    f'{year}-1-1', f'{year}-12-31')).all()]
                [r.pop('_sa_instance_state', None) for r in result]
                self.response.body = result
        else:
            super().read()

    def update(self, body, **kwargs):
        try:
            logging.info(f'Modifiying table {self.entityClass.table_name}')
            new_feriado = self.entityClass(**body)

            with session_scope() as s:
                current = s.query(self.entityClass).filter(self.entityClass.id == new_feriado.id).first()
                current.fecha = new_feriado.fecha
                current.descripcion = new_feriado.descripcion
                current.ultima_modificacion = datetime.now()
                current.usuario_ultima_modificacion = new_feriado.usuario_ultima_modificacion
            self.response.body = f'Objeto {current.id} en {self.entityClass.table_name} modificado'

        except IntegrityError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e


class ControllerPractica(BaseController):
    def __init__(self):
        super().__init__()
        self.entityClass = Entities.Practica

    def read(self, **kwargs):
        id_obj = ''
        id_prest = kwargs.get('id_prestador')
        id_pac = kwargs.get('id_paciente')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        filter_expr = None

        if id_prest and id_pac:
            pass
        elif id_prest:
            id_obj = id_prest
            filter_expr = self.entityClass.prestador
        elif id_pac:
            id_obj = id_pac
            filter_expr = self.entityClass.paciente

        if id_prest and id_pac and start_date and end_date:
            with session_scope() as s:
                result = [vars(r) for r in s.query(self.entityClass).filter(
                    self.entityClass.paciente == id_pac,
                    self.entityClass.prestador == id_prest,
                    between(self.entityClass.fecha, start_date, end_date)).all()
                ]
                [r.pop('_sa_instance_state', None) for r in result]
                self.response.body = result

        elif (start_date and end_date) and (id_prest or id_pac):
            with session_scope() as s:
                result = [vars(r) for r in s.query(self.entityClass).filter(
                    filter_expr == id_obj,
                    between(self.entityClass.fecha, start_date, end_date)).all()
                          ]
            [r.pop('_sa_instance_state', None) for r in result]
            self.response.body = result

        elif (start_date and end_date) and not(id_prest and id_pac):
            with session_scope() as s:
                result = [vars(r) for r in s.query(self.entityClass).filter(
                    between(self.entityClass.fecha, start_date, end_date)).all()
                          ]
            [r.pop('_sa_instance_state', None) for r in result]
            self.response.body = result

        else:
            super().read()

    def update(self, body, **kwargs):
        try:
            logging.info(f'Modifiying table {self.entityClass.table_name}')
            new_practica = self.entityClass(**body)

            with session_scope() as s:
                current = s.query(self.entityClass).filter(self.entityClass.id == new_practica.id).first()
                current.fecha = new_practica.fecha
                current.descripcion = new_practica.descripcion
                current.ultima_modificacion = datetime.now()
                current.usuario_ultima_modificacion = new_practica.usuario_ultima_modificacion
            self.response.body = f'Objeto {current.id} en {self.entityClass.table_name} modificado'

        except IntegrityError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e

    def create(self, body, **kwargs):

        if type(body) != list:
            raise ValueError("body must be a list of practicas")

        errors = []
        np_paciente = None
        np_prestador = None
        np_modulo = None
        np_sub_modulo = None
        np_observacion_paciente = None
        np_observacion_prestador = None

        for prac in body:
            logging.info(f"INSERTING: {json.dumps(prac)}")
            new_practica = self.entityClass(**prac)
            np_paciente = new_practica.paciente
            np_prestador = new_practica.prestador
            np_modulo = new_practica.modulo
            np_sub_modulo = new_practica.sub_modulo
            np_observacion_paciente = new_practica.observaciones_paciente
            np_observacion_prestador = new_practica.observaciones_prestador
            try:
                with session_scope() as s:
                    s.add(new_practica)
                    logging.info("object added")
            except Exception as e:
                logging.error(e)
                errors.append({'date': new_practica.fecha, 'err': e})

        self.response.code = 200
        self.response.body = errors

        if len(body) != len(errors) or type(body) != list:
            logging.info('review if paciente or prestador needs to be update')
            try:
                with session_scope() as s:
                    pac = s.query(Entities.Paciente).filter(Entities.Paciente.id == np_paciente).first()
                    prest = s.query(Entities.Prestador).filter(Entities.Prestador.id == np_prestador).first()

                    if pac.modulo != np_modulo or \
                       pac.sub_modulo != np_sub_modulo or \
                       pac.observacion != np_observacion_paciente:

                        pac.modulo = np_modulo
                        pac.sub_modulo = np_sub_modulo
                        pac.observacion = np_observacion_paciente
                        logging.info("updated PACIENTE")

                    if prest.comentario != np_observacion_prestador:
                        prest.comentario = np_observacion_prestador
                        logging.info("updated PRESTADOR")

            except Exception as e:
                logging.error(e)
                print(e)


class ControllerAdmin:

    def __init__(self):
        self.response = Response()

    def update(self, body):
        logging.info(f'post method body: {body}')
        try:
            if body['operation'] == 'recreate':
                logging.info("dropping DB")
                drop_database(engine.url)
                self.response.body = 'DB dropped'
                logging.info('Create tables operation')
                if not database_exists(engine.url):
                    logging.info('DB must be created')
                    create_database(engine.url)
                    logging.info('DB created')

                logging.info('creating tables')
                Base.metadata.create_all(engine)
                self.response.body = 'db create operation finished'

        except Exception as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e

    def read(self):
        self.response.body = "Service is working"