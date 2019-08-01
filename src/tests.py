from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from common import RDSConfig
from models import Base, Prestador
from services import DataBrokerService
import json

engine = create_engine(RDSConfig.ENGINE)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def insert_test():
    new_perstador = Prestador(nombre='manuel', apellido='palacios', CUIT='20-29188989-2')
    session.add(new_perstador)
    session.commit()

def query_test():
    R = session.query(Prestador).all()
    for a in R:
        print(vars(a))


def service_test():
    s = DataBrokerService()
    s.get_tables(['PRESTADORES'])
    print(s.response.service_response)

service_test()