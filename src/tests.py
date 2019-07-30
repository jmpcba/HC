import os
import main
import common
import requests
from service import DataBrokerService

sql = []
for n in range(5, 500):
    sql.append (f'INSERT INTO DESARROLLO.PRESTADORES (CUIT, NOMBRE) VALUES ("CUIT-{n}", "nombre-{n}");')

rds = common.RDS()
rds.statement(sql)


