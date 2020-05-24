from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Prestador(Base):
    __tablename__ = 'PRESTADORES'
    id = Column(Integer, primary_key=True, autoincrement=True)
    CUIT = Column(String(50), primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    mail = Column(String(150), nullable=False)
    especialidad = Column(String(150), primary_key=True)
    servicio = Column(String(150), nullable=False)
    localidad = Column(String(150), nullable=False, primary_key=True)
    monto_feriado = Column(Float(2), nullable=False)
    monto_semana = Column(Float(2), nullable=False)
    monto_fijo = Column(Float(2), nullable=False)
    monto_diferencial = Column(Float(2), nullable=False)
    zona = Column(Integer, ForeignKey('ZONAS.id'))
    comentario = Column(String(150), nullable=False)
    baja = Column(Boolean, default=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(String(50), nullable=False)

    @property
    def table_name(self):
        return self.__tablename__


class Paciente(Base):
    __tablename__ = 'PACIENTES'
    afiliado = Column(String(50), primary_key=True)
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
    usuario_ultima_modificacion = Column(String(50), nullable=False)

    @property
    def table_name(self):
        return self.__tablename__


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
    usuario_ultima_modificacion = Column(String(50), nullable=False)

    @property
    def table_name(self):
        return self.__tablename__


class SubModulo(Base):
    __tablename__ = 'SUB_MODULOS'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(20), unique=True)
    descripcion = Column(String(50), nullable=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(String(50), nullable=False)

    @property
    def table_name(self):
        return self.__tablename__


class Practica(Base):
    __tablename__ = 'PRACTICAS'
    id = Column(Integer, autoincrement=True)
    paciente = Column(String(50), ForeignKey('PACIENTES.afiliado'), primary_key=True)
    modulo = Column(Integer, ForeignKey('MODULOS.id'))
    sub_modulo = Column(Integer, ForeignKey('SUB_MODULOS.id'))
    prestador = Column(Integer, ForeignKey('PRESTADORES.id'), primary_key=True)
    hs_normales = Column(Float(2), nullable=False)
    hs_feriados = Column(Float(2), nullable=False)
    hs_diferencial = Column(Float(2), nullable=False)
    fecha = Column(Date, nullable=False, primary_key=True)
    observaciones = Column(String(200), nullable=False)
    observaciones_paciente = Column(String(200))
    observaciones_prestador = Column(String(200))
    ultima_modificacion = Column(Date)
    usuario_ultima_modificacion = Column(String(50), nullable=False)

    @property
    def table_name(self):
        return self.__tablename__


class Zona(Base):
    __tablename__ = 'ZONAS'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    mail = Column(String(50), nullable=False)
    pwd = Column(String(50), nullable=False)
    propietario = Column(String(50), nullable=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(String(50), nullable=False)

    @property
    def table_name(self):
        return self.__tablename__


class Liquidacion(Base):
    __tablename__ = 'LIQUIDACION'
    id = Column(Integer, primary_key=True)
    cuit = Column(String(50), primary_key=True)
    localidad = Column(String(50), primary_key=True)
    especialidad = Column(String(50), primary_key=True)
    mes = Column(Date, primary_key=True)
    id_prest = Column(Integer, ForeignKey('PRESTADORES.id'))
    hs_normales = Column(Float(2), nullable=False)
    hs_feriados = Column(Float(2), nullable=False)
    hs_diferencial = Column(Float(2), nullable=False)
    importe_normal = Column(Float(2), nullable=False)
    importe_feriado = Column(Float(2), nullable=False)
    importe_diferencial = Column(Float(2), nullable=False)
    monto_fijo = Column(Float(2), nullable=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(String(50), nullable=False)

    @property
    def table_name(self):
        return self.__tablename__


class Feriado(Base):
    __tablename__ = 'FERIADOS'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, unique=True)
    descripcion = Column(String(50), nullable=False)
    ultima_modificacion = Column(Date, nullable=False)
    usuario_ultima_modificacion = Column(String(50), nullable=False)

    @property
    def table_name(self):
        return self.__tablename__


class Especialidad(Base):
    __tablename__ = 'ESPECIALIDADES'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)

    @property
    def table_name(self):
        return self.__tablename__