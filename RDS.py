import os
import json
from enum import Enum
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Prestador(Base):
    __tablename__ = 'PRESTADORES'
    id = Column(Integer, primary_key= True)
    CUIT = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    mail = Column(String(150), nullable=False)
    especialidad = Column(String(150), nullable=False, unique=True)
    servicio = Column(String(150), nullable=False)
    localidad = Column(String(150), nullable=False, unique=True)
    monto_feriado = Column(Float(2), nullable=False)
    monto_semana = Column(Float(2), nullable=False)
    monto_fijo = Column(Float(2), nullable=False)
    zona = Column(Integer, ForeignKey('ZONAS.id'))
    comentario = Column(String(150), nullable=False)
    baja = Column(Boolean, nullable=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(Integer, ForeignKey('USUARIOS.id'))


class Paciente(Base):
    __tablename__ = 'PACIENTES'
    id = Column(Integer, primary_key=True)
    afiliado = Column(String(50), unique=True)
    DNI = Column(String(50), nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    localidad = Column(String(50), nullable=False)
    obra_social = Column(String(50), nullable=False)
    observacion = Column(String(50), nullable=False)
    modulo = Column(Integer, ForeignKey('MODULOS.id'))
    sub_modulo = Column(Integer, ForeignKey('SUB_MODULOS.id'))
    baja = Column(Boolean, default=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(Integer, ForeignKey('USUARIOS.id'))

    
class Modulo(Base):
    __tablename__ = 'MODULOS'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(20), unique=True)
    medico = Column(Float(2), nullable=False)
    enfermeria = Column(Float(2), nullable=False)
    kinesiologia = Column(Float(2), nullable=False)
    fonoaudiologia = Column(Float(2), nullable=False)
    cuidador = Column(Float(2), nullable=False)
    nutricion = Column(Float(2), nullable=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(Integer, ForeignKey('USUARIOS.id'))


class SubModulo(Base):
    __tablename__ = 'SUB_MODULOS'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(20), unique=True)
    descripcion = Column(String(50), nullable=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(Integer, ForeignKey('USUARIOS.id'))


class Practica(Base):
    __tablename__ = 'PRACTICAS'
    id = Column(Integer, primary_key=True)
    cuit = Column(String(50), nullable=False)
    afiliado = Column(Integer, ForeignKey('PACIENTES.id'), unique=True)
    modulo = Column(Integer, ForeignKey('MODULOS.id'), unique=True)
    sub_modulo = Column(Integer, ForeignKey('SUB_MODULOS.id'), unique=True)
    id_prest = Column(Integer, ForeignKey('PRESTADORES.id'), unique=True)
    hs_normales = Column(Float(2), nullable=False)
    hs_feriados = Column(Float(2), nullable=False)
    hs_diferencial = Column(Float(2), nullable=False)
    fecha = Column(Date, nullable=False, unique=True)
    observaciones = Column(String(200), nullable=False)
    observaciones_paciente = Column(String(200))
    observaciones_prestacion = Column(String(200))
    ultima_modificacion = Column(Date)
    usuario_ultima_modificacion = Column(Integer, ForeignKey('USUARIOS.id'))


class Zona(Base):
    __tablename__ = 'ZONAS'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    mail = Column(String(50), nullable=False)
    pwd = Column(String(50), nullable=False)
    propietario = Column(String(50), nullable=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(Integer, ForeignKey('USUARIOS.id'))


class Usuario(Base):
    __tablename__ = 'USUARIOS'
    id = Column(Integer, primary_key=True)
    DNI = Column(String(50), unique=True)
    apellido = Column(String(50), nullable=False)
    nombre = Column(String(50), nullable=False)
    nivel = Column(String(50), nullable=False)
    pwd = Column(String(50), nullable=False)
    ultima_modificacion = Column(Date, nullable=False)


class Liquidacion(Base):
    __tablename__ = 'LIQUIDACION'
    id = Column(Integer, primary_key=True)
    cuit = Column(String(50), unique=True)
    localidad = Column(String(50), unique=True)
    especialidad = Column(String(50), unique=True)
    mes = Column(Date, unique=True)
    id_prest = Column(Integer, ForeignKey('PRESTADORES.id'))
    hs_normales = Column(Float(2), nullable=False)
    hs_feriados = Column(Float(2), nullable=False)
    hs_diferencial = Column(Float(2), nullable=False)
    importe_normal = Column(Float(2), nullable=False)
    importe_feriado = Column(Float(2), nullable=False)
    importe_diferencial = Column(Float(2), nullable=False)
    monto_fijo = Column(Float(2), nullable=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(Integer, ForeignKey('USUARIOS.id'))


class Feriado(Base):
    __tablename__ = 'FERIADOS'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, unique=True)
    descripcion = Column(String(50), nullable=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(Integer, ForeignKey('USUARIOS.id'))


class Especialidad(Base):
    __tablename__ = 'ESPECIALIDADES'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)


class RDSConfig:
    # TODO pasar endpoint base de datos a variable de entorno
    # hacer un test, si no da 200 hacer un roll back
    RDS_HOST = "hc-rds-dev.cluster-c0rtb6x1vjcr.us-east-1.rds.amazonaws.com"
    try:
        USER = os.environ['DB_USER']
        PWD = os.environ['DB_PASSWORD']
    except KeyError:
        USER = ''
        PWD = ''
    DB = 'HC_DEV'
    DIALECT = 'mysql+pymysql'
    ENGINE = f'{DIALECT}://{USER}:{PWD}@{RDS_HOST}/{DB}'


class Resources(Enum):
    PRESTADOR = 'PRESTADOR'
    PACIENTE = 'PACIENTE'
    MODULO = 'MODULO'
    SUBMODULO = 'SUBMODULO'
    LIQUIDACION = 'LIQUIDACION'
    ZONA = 'ZONA'
    USUARIO = 'USUARIO'
    FERIADO = 'FERIADO',
    ESPECIALIDAD = 'ESPECIALIDAD'
    ADMIN = 'ADMIN'
    PRACTICA = 'PRACTICA'


class RDSModel:

    def __init__(self, resource):
        models = {
            Resources.PRESTADOR.value: Prestador,
            Resources.PACIENTE.value: Paciente,
            Resources.MODULO.value: Modulo,
            Resources.SUBMODULO.value: SubModulo,
            Resources.LIQUIDACION.value: Liquidacion,
            Resources.ZONA.value: Zona,
            Resources.USUARIO.value: Usuario,
            Resources.FERIADO.value: Feriado,
            Resources.ESPECIALIDAD.value: Especialidad,
            Resources.PRACTICA.value: Practica,
        }

        self._model = models[resource]

    @property
    def model_map(self):
        return self._model

    @property
    def table_name(self):
        return self._model.__tablename__