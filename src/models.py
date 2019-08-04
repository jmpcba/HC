from lib.sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, ForeignKey
from lib.sqlalchemy.orm import relationship
from lib.sqlalchemy.ext.declarative import declarative_base
from lib.sqlalchemy import create_engine
import json

Base = declarative_base()


class Prestador(Base):
    __tablename__ = 'PRESTADORES'
    id = Column(Integer, primary_key= True)
    CUIT = Column(String(50), nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    mail = Column(String(150), nullable=False)
    especialidad = Column(String(150), nullable=False)
    servicio = Column(String(150), nullable=False)
    localidad = Column(String(150), nullable=False)
    monto_feriado = Column(Float(2), nullable=False)
    monto_semana = Column(Float(2), nullable=False)
    monto_fijo = Column(Float(2), nullable=False)
    zona = Column(Integer, ForeignKey('ZONAS.id'))
    comentario = Column(String(150), nullable=False)
    baja = Column(Boolean, nullable=False)


class Paciente(Base):
    __tablename__ = 'PACIENTES'
    afiliado = Column(String(20), primary_key= True)
    DNI = Column(String(50), nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    localidad = Column(String(50), nullable=False)
    obra_social = Column(String(50), nullable=False)
    observacion = Column(String(50), nullable=False)
    modulo = Column(String(20), ForeignKey('MODULOS.codigo'))
    sub_modulo = Column(String(20), ForeignKey('SUB_MODULOS.codigo'))
    baja = Column(Boolean, default=False)


class Modulo(Base):
    __tablename__ = 'MODULOS'
    codigo = Column(String(20), primary_key=True)
    medico = Column(Float(2), nullable=False)
    enfermeria = Column(Float(2), nullable=False)
    kinesiologia = Column(Float(2), nullable=False)
    fonoaudiologia = Column(Float(2), nullable=False)
    cuidador = Column(Float(2), nullable=False)
    nutricion = Column(Float(2), nullable=False)
    

class SubModulo(Base):
    __tablename__ = 'SUB_MODULOS'
    codigo = Column(String(20), primary_key=True)
    descripcion = Column(String(50), nullable=False)


class Liquidacion(Base):
    __tablename__ = 'LIQUIDACIONES'
    id = Column(Integer, primary_key=True)
    cuit = Column(String(50), nullable=False)
    localidad = Column(String(50), nullable=False)
    especialidad = Column(String(50), nullable=False)
    mes = Column(String(50), nullable=False)
    id_prest = Column(Integer, ForeignKey('PRESTADORES.id'))
    hs_normales = Column(Float(2), nullable=False)
    hs_feriados = Column(Float(2), nullable=False)
    hs_diferencial = Column(Float(2), nullable=False)
    importe_normal = Column(Float(2), nullable=False)
    importe_feriado = Column(Float(2), nullable=False)
    importe_diferencial = Column(Float(2), nullable=False)
    monto_fijo = Column(Float(2), nullable=False)


class Zona(Base):
    __tablename__ = 'ZONAS'
    id = Column(Integer, primary_key= True)
    nombre = Column(String(50), nullable=False)
    mail = Column(String(50), nullable=False)
    pwd = Column(String(50), nullable=False)
    propietario = Column(String(50), nullable=False)


class RDSConfig:
    RDS_HOST = "dev-database-1.c0rtb6x1vjcr.us-east-1.rds.amazonaws.com"
    NAME = 'admin'
    #PWD = os.environ['db_password']
    PWD = 'Newuser1!'
    DB = 'HC_ORM'
    DIALECT = 'mysql+pymysql'
    ENGINE = f'{DIALECT}://{NAME}:{PWD}@{RDS_HOST}/{DB}'

    TABLES = [
    {'table_name': 'PRESTADORES', 'model': Paciente},
    {'table_name': 'PACIENTES', 'model': Paciente},
    {'table_name': 'MODULOS', 'model': Modulo},
    {'table_name': 'SUB_MODULOS', 'model': SubModulo},
    {'table_name': 'LIQUIDACIONES', 'model': Liquidacion},
    {'table_name': 'ZONAS', 'model': Zona},
    ]


def create_tables():
        engine = create_engine(RDSConfig.ENGINE, echo=True)
        Base.metadata.create_all(engine)