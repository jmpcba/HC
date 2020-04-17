import cfg


"""
dev_url = https://cl86zb12f8.execute-api.us-east-1.amazonaws.com/DEV
prod_url = 
rds_dev_endpoint = hc-rds-dev.cluster-c0rtb6x1vjcr.us-east-1.rds.amazonaws.com


def insert_test():
    new_prestador = Prestador(nombre='manuel', apellido='palacios', CUIT='20-29188989-2')
    session.add(new_prestador)
    session.commit()

def query_test():
    R = session.query(Prestador).all()
    for a in R:
        print(vars(a))


def service_test():
    s = DataBrokerService()
    s.get(['PRESTADORES', 'PACIENTES'])
    print(s.response.service_response)

def get_prestador():
        s = PrestadoresService()
        print(s.get(1))

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
        s.post(payload)

        print(s.response.service_response)

def put_test():
        payload = {'id': 1, 
                'CUIT': '20-29-188989-2', 
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
        s.put(payload)

        print(s.response.service_response)

def post_prestador_service():
        url = 'https://2idw8jlsf6.execute-api.us-east-1.amazonaws.com/prod/v1/prestador'
        payload = {"id":None,"cuit":"10--11223344-3-9","nombre":"alberto","apellido":"perez","especialidad":"ENFERMERIA","localidad":"la loma del culo","email":"jmpcba@gmail.com","obraSocial":"daspu","montoNormal":100.0,"montoFeriado":120.0,"montoFijo":200.0,"montoDiferencial":150.0,"fechaCese":"2019-08-11T00:00:00","observaciones":"ninguna","modifUser":29188989,"creoUser":29188989,"fechaCarga":"2019-08-11T00:00:00-03:00","fechaMod":"2019-08-11T00:00:00-03:00",
"estado":0,"zona":1,"modificado":False}
        r = requests.post(url, data=payload)
        print(r)

engine = create_engine(RDSConfig.ENGINE)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


"""


if __name__ == '__main__':
        s = cfg.Setup('dev')
        s.test_up()
