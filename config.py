import os


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
