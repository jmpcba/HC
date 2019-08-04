from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Prestador, RDSConfig
from services import DataBrokerService, PrestadoresService
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

def post_test():
        payload = {'CUIT': '20-29-188989-2', 
                'nombre': 'juan manuel',
                'apellido': 'palacios',
                'mail': 'jmpcba@gmail.com',
                'especialidad': 'enfermeria',
                'servicio': 'pami',
                'localidad': 'cordoba',
                'monto_feriado': 100,
                'monto_semana': 150,
                'monto_fijo': 50,
                'zona': 1,
                'comentario': 'un comentario',
                'baja': 0}
        s = PrestadoresService()
        s.insert(payload)

        print(s.response.service_response)

def put_test():
        payload = {'id': 1, 
                'CUIT': '20-29-188989-2', 
                'nombre': 'juan manuel',
                'apellido': 'palacios',
                'mail': 'jmpcba@gmail.com',
                'especialidad': 'enfermeria',
                'servicio': 'pami',
                'localida': 'cba',
                'monto_feriado': 100,
                'monto_semana': 150,
                'monto_fijo': 50,
                'zona': 1,
                'comentario': 'un comentario',
                'baja': 0}
        
        s = PrestadoresService()
        s.update(payload)

        print(s.response.service_response)

put_test()

