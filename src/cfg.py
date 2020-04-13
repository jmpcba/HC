import argparse
import logging
import requests
import json


class Setup:

    def __init__(self, environment):
        urls = {
            'dev': 'https://cl86zb12f8.execute-api.us-east-1.amazonaws.com/DEV/v1/ADMIN',
            'prod': 'https://cl86zb12f8.execute-api.us-east-1.amazonaws.com/PROD'
        }

        self.url = urls[environment]
        
    def test_up(self):
        r = requests.get(self.url)
        print(f'CODE: {r.status_code}')
        print(f'MESSAGE: {r.text}')
    
    def create_tables(self):
        payload = {"operation":"create"}
        r = requests.post(self.url, data=json.dumps(payload))
        print(f'CODE: {r.status_code}')
        print(f'MESSAGE: {r.text}')

    def drop(self):
        payload = {"operation":"drop"}
        r = requests.post(self.url, data=json.dumps(payload))
        print(f'CODE: {r.status_code}')
        print(f'MESSAGE: {r.text}')

    def create_user(self):
        usr_url = 'https://cl86zb12f8.execute-api.us-east-1.amazonaws.com/DEV/v1/USUARIO'
        payload = {
            'DNI': '29188989',
            'apellido': 'palacios',
            'nombre': 'juan manuel',
            'nivel': 0,
            'pwd': 'noimportaahora',
            'usuario_ultima_modificacion': ''
        }
        r = requests.post(usr_url, json.dumps(payload))
        print(f'CODE: {r.status_code}')
        print(f'MESSAGE: {r.text}')


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='DB setup options')
    parser.add_argument('operation', help='what operation do you want to execute?', choices=['create','adduser', 'drop'])
    args = parser.parse_args()
    admin = Setup('dev')
    
    if args.operation == 'create':
        admin.create_tables()
    elif args.operation == 'adduser':
        admin.create_user()
    elif args.operation == 'drop':
        admin.drop()
