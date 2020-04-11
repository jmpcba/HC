import os
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import json

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
    usuario_ultima_modificacion = Column(String(50), ForeignKey('USUARIOS.DNI'))


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
    modulo = Column(String(20), ForeignKey('MODULOS.codigo'))
    sub_modulo = Column(String(20), ForeignKey('SUB_MODULOS.codigo'))
    baja = Column(Boolean, default=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(String(50), ForeignKey('USUARIOS.DNI'))

    
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
    usuario_ultima_modificacion = Column(String(50), ForeignKey('USUARIOS.DNI'))


class SubModulo(Base):
    __tablename__ = 'SUB_MODULOS'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(20), unique=True)
    descripcion = Column(String(50), nullable=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(String(50), ForeignKey('USUARIOS.DNI'))


class Practica(Base):
    __tablename__ = 'PRACTICAS'
    id = Column(Integer, primary_key=True)
    cuit = Column(String(50), nullable=False)
    afiliado = Column(String, ForeignKey('PACIENTES.id'), unique=True)
    modulo = Column(String, ForeignKey('MODULOS.codigo'), unique=True)
    sub_modulo = Column(String, ForeignKey('SUB_MODULOS.codigo'), unique=True)
    id_prest = Column(Integer, ForeignKey('PRESTADORES.id'), unique=True)
    hs_normales = Column(Float(2), nullable=False)
    hs_feriados = Column(Float(2), nullable=False)
    hs_diferencial = Column(Float(2), nullable=False)
    fecha = Column(Date, nullable=False, unique=True)
    observaciones = Column(String, nullable=False)
    observaciones_paciente = Column(String)
    observaciones_prestacion = Column(String)
    ultima_modificacion = Column(Date)
    usuario_ultima_modificacion = Column(String(50), ForeignKey('USUARIOS.DNI'))


class Zona(Base):
    __tablename__ = 'ZONAS'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    mail = Column(String(50), nullable=False)
    pwd = Column(String(50), nullable=False)
    propietario = Column(String(50), nullable=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(String(50), ForeignKey('USUARIOS.DNI'))


class Usuario(Base):
    __tablename__ = 'USUARIOS'
    id = Column(Integer, primary_key=True)
    DNI = Column(String, unique=True)
    apellido = Column(String(50), nullable=False)
    nombre = Column(String(50), nullable=False)
    nivel = Column(String(50), nullable=False)
    pwd = Column(String(50), nullable=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(String(50), ForeignKey('USUARIOS.DNI'))


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
    usuario_ultima_modificacion = Column(String(50), ForeignKey('USUARIOS.DNI'))


class Feriado(Base):
    __tablename__ = 'FERIADOS'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, unique=True)
    descripcion = Column(String(50), nullable=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(String(50), ForeignKey('USUARIOS.DNI'))


class Especialidad(Base):
    __tablename__ = 'ESPECIALIDADES'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)


class RDSConfig:
    # TODO pasar endpoint base de datos a variable de entorno
    RDS_HOST = "hc-rds-dev.cluster-c0rtb6x1vjcr.us-east-1.rds.amazonaws.com"
    NAME = 'admin'
    PWD = os.environ['DB_PASSWORD']
    DB = 'HC_DEV'
    DIALECT = 'mysql+pymysql'
    ENGINE = f'{DIALECT}://{NAME}:{PWD}@{RDS_HOST}/{DB}'

    PRESTADORES = 'PRESTADORES'
    PACIENTES = 'PACIENTES'
    MODULOS = 'MODULOS'
    SUB_MODULOS = 'SUB_MODULOS'
    ZONAS = 'ZONAS'
    PRACTICAS = 'PRACTICAS'
    USUARIOS = 'USUARIOS'
    LIQUIDACION = 'LIQUIDACION'
    FERIADOS = 'FERIADOS'
    ESPECIALIDADES = 'ESPECIALIDADES'

    TABLES = [
        {'table_name': PRESTADORES, 'model': Prestador},
        {'table_name': PACIENTES, 'model': Paciente},
        {'table_name': MODULOS, 'model': Modulo},
        {'table_name': SUB_MODULOS, 'model': SubModulo},
        {'table_name': LIQUIDACION, 'model': Prestador},
        {'table_name': ZONAS, 'model': Zona},
        {'table_name': USUARIOS, 'model': Usuario},
        {'table_name': LIQUIDACION, 'model': Liquidacion},
        {'table_name': FERIADOS, 'model': Feriado},
        {'table_name': ESPECIALIDADES, 'model': Especialidad},
    ]
    

def create_tables():
    engine = create_engine(RDSConfig.ENGINE, echo=True)
    Base.metadata.create_all(engine)
