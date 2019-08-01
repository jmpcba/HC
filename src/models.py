from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class Prestador(Base):
    __tablename__ = 'PRESTADORES'
    id = Column(Integer, primary_key= True)
    CUIT = Column(String(50), nullable=False)
    nombre = Column(String(50), nullable=False)
"""
class Paciente(Base):
    pass
class Modulo(Base):
    pass
class SubModulo(Base):
    pass
class Liquidacion(Base):
    pass 
"""