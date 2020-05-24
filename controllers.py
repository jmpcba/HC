import logging
import json
import entities
from datetime import datetime
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy import create_engine, between, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func, label
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError, StatementError
from pymysql import MySQLError
from entities import Base
from config import RDSConfig
from entities import Paciente, Practica, Prestador, Modulo, SubModulo

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
        self.entityClass = entities.Zona

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
                self.response.body = f'Objeto {new_zona.id} modificado'

        except IntegrityError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e


class ControllerModulo(BaseController):
    def __init__(self):
        super().__init__()
        self.entityClass = entities.Modulo

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
            self.response.body = f'Objeto {new_modulo.id} en {self.entityClass.table_name} modificado'

        except IntegrityError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e


class ControllerSubModulo(BaseController):
    def __init__(self):
        super().__init__()
        self.entityClass = entities.SubModulo

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
            self.response.body = f'Objeto {new_sub_modulo.id} en {self.entityClass.table_name} modificado'

        except IntegrityError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e


class ControllerPrestador(BaseController):
    def __init__(self):
        super().__init__()
        self.entityClass = entities.Prestador

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
            self.response.body = f'Objeto {new_prestador.id} en {self.entityClass.table_name} modificado'

        except IntegrityError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e


class ControllerPaciente(BaseController):
    def __init__(self):
        super().__init__()
        self.entityClass = entities.Paciente

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
            self.response.body = f'Objeto {new_paciente.id} en {self.entityClass.table_name} modificado'

        except IntegrityError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e


class ControllerFeriado(BaseController):
    def __init__(self):
        super().__init__()
        self.entityClass = entities.Feriado

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
            self.response.body = f'Objeto {new_feriado.id} en {self.entityClass.table_name} modificado'

        except IntegrityError as e:
            logging.error(e)
            self.response.code = 500
            self.response.body = e


class ControllerPractica(BaseController):
    def __init__(self):
        super().__init__()
        self.entityClass = entities.Practica

    def read(self, **kwargs):
        id_prest = kwargs.get('id_prestador')
        id_pac = kwargs.get('id_paciente')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        query_class = None
        id_obj = None

        logging.info(f'Fetching practicas with parameters:\n\
            PRESTADOR: {id_prest}\n \
            PACIENTE: {id_pac}\n\
            START DATE: {start_date}\n\
            END_DATE: {end_date}')

        if start_date:
            y = int(start_date[start_date.rfind('/') + 1: start_date.rfind('/') + 5])
            d = int(start_date[start_date.find('/') + 1: start_date.rfind('/')])
            m = int(start_date[:start_date.find('/')])
            start_date = datetime(y, m, d)

        if end_date:
            y = int(end_date[end_date.rfind('/') + 1: end_date.rfind('/') + 5])
            d = int(end_date[end_date.find('/') + 1: end_date.rfind('/')])
            m = int(end_date[:end_date.find('/')])
            end_date = datetime(y, m, d)

        if id_prest and id_pac:
            self.response.body = 'utilice solo id_prestador o id_paciente como filtros. No pueden usarse ambos a la vez'
            self.response.code = 500
        elif id_prest:
            id_obj = id_prest
            query_class = PracticasPrestador()
        elif id_pac:
            id_obj = id_pac
            query_class = PracticasPaciente()

        if id_obj and query_class:
            try:
                self.response.body = query_class.get_practicas(start_date, end_date, id_obj)
                self.response.code = 200

            except MySQLError as e:
                self.response.body = e
                self.response.code = 500
        
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
            self.response.body = f'Objeto {new_practica.id} en {self.entityClass.table_name} modificado'

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
                err = e
                if "1062" in e.args[0]:
                    err = "Ya existe una practica para esta fecha/prestador/paciente"
                errors.append({'date': new_practica.fecha, 'err': err})

        self.response.code = 200
        self.response.body = errors

        if len(body) != len(errors) or type(body) != list:
            logging.info('review if paciente or prestador needs to be update')
            try:
                with session_scope() as s:
                    pac = s.query(entities.Paciente).filter(entities.Paciente.id == np_paciente).first()
                    prest = s.query(entities.Prestador).filter(entities.Prestador.id == np_prestador).first()

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

    def _parse_read_result(self, result):
        ret = []
        for r in result:
            d = {
               'afiliado': r.afiliado,
                'CUIT': r.CUIT,
                'apellido': r.apellido,
                'nombre': r.nombre,
                'fecha': r.fecha,
                'Modulo': r[5],
                'SubModulo': r.descripcion,
                'hs_normales': r.hs_normales,
                'hs_feriados': r.hs_feriados,
                'hs_diferencial': r.hs_diferencial,
                'monto_semana': r.monto_semana,
                'monto_feriado': r.monto_feriado,
                'monto_diferencial': r.monto_diferencial
            }
            ret.append(d)
        return ret


class PracticasBase:

    DETAIL_COLUMNS = [
                    Prestador.CUIT,
                    Paciente.afiliado,
                    Practica.fecha,
                    Modulo.codigo,
                    SubModulo.codigo,
                    SubModulo.descripcion,
                    Practica.hs_normales,
                    Practica.hs_feriados,
                    Practica.hs_diferencial,
                    (Prestador.monto_semana * Practica.hs_normales).label('monto_semana'),
                    (Prestador.monto_feriado * Practica.hs_feriados).label('monto_feriado'),
                    (Prestador.monto_diferencial * Practica.hs_diferencial).label('monto_diferencial')
                    ]

    SUMMARY_COLUMNS = [
        Prestador.CUIT,
        func.count(Practica.id),
        func.sum(Practica.hs_feriados).label('hs_feriados'),
        func.sum(Practica.hs_normales).label('hs_normales'),
        func.sum(Practica.hs_diferencial).label('hs_diferencial')
        ]


class PracticasPaciente(PracticasBase):

    def get_practicas(self, start_date, end_date, id_paciente):
        self.DETAIL_COLUMNS += [
            Prestador.nombre,
            Prestador.apellido,
        ]

        self.SUMMARY_COLUMNS += [
            Prestador.nombre,
            Prestador.apellido,
        ]
        with session_scope() as s:
            detail_result = s.query(*self.DETAIL_COLUMNS) \
                .join(Paciente, Practica.paciente == Paciente.id) \
                .join(Prestador, Practica.prestador == Prestador.id) \
                .join(Modulo, Practica.modulo == Modulo.id) \
                .join(SubModulo, Practica.sub_modulo == SubModulo.id)\
                .filter(
                    Paciente.id == id_paciente,
                    between(
                        Practica.fecha,
                        start_date,
                        end_date
                    )
            ).all()

            summary_result = s.query(*self.SUMMARY_COLUMNS) \
                .join(Prestador, Practica.prestador == Prestador.id) \
                .filter(
                    Paciente.id == id_paciente,
                    between(
                        Practica.fecha,
                        start_date,
                        end_date
                    )
                ).group_by(
                    Prestador.CUIT,
                    Prestador.apellido,
                    Prestador.nombre,
                    Prestador.especialidad,
                    ).all()

        return {'detail': [r._asdict() for r in detail_result], 'summary': [r._asdict() for r in summary_result]}


class PracticasPrestador(PracticasBase):
    def get_practicas(self, start_date, end_date, id_paciente):
        self.DETAIL_COLUMNS += [
            Paciente.nombre,
            Paciente.apellido,
        ]

        self.SUMMARY_COLUMNS += [
            Paciente.nombre,
            Paciente.apellido,
        ]
        with session_scope() as s:
            detail_result = s.query(*self.DETAIL_COLUMNS) \
                .join(Paciente, Practica.paciente == Paciente.id) \
                .join(Prestador, Practica.prestador == Prestador.id) \
                .join(Modulo, Practica.modulo == Modulo.id) \
                .join(SubModulo, Practica.sub_modulo == SubModulo.id) \
                .filter(
                Paciente.id == id_paciente,
                between(
                    Practica.fecha,
                    start_date,
                    end_date
                )
            ).all()

            summary_result = s.query(*self.SUMMARY_COLUMNS) \
                .join(Prestador, Practica.prestador == Prestador.id) \
                .filter(
                Paciente.id == id_paciente,
                between(
                    Practica.fecha,
                    start_date,
                    end_date
                )
            ).group_by(
                Prestador.CUIT,
                Prestador.apellido,
                Prestador.nombre,
                Prestador.especialidad,
            ).all()

        return {'detail': [r._asdict() for r in detail_result], 'summary': [r._asdict() for r in summary_result]}


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
