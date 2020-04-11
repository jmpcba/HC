from sqlalchemy.ext.declarative import declarative_base
import argparse
import logging
import models
import requests


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
            body = {'operation':'create'}
            r = requests.post(self.url, data=body)
            print(f'CODE: {r.status_code}')
            print(f'MESSAGE: {r.text}')


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='DB setup options')
    parser.add_argument('operation', help='what operation do you want to execute?', choices=['create',])
    args = parser.parse_args()
    admin = Setup('dev')
    
    if args.operation == 'create':
        admin.create_tables()
