import os
import requests


def test_databroker():
    endpoint = 'https://2idw8jlsf6.execute-api.us-east-1.amazonaws.com/prod/v1/databroker?tables=prestadores,pacientes'
    r = requests.get(endpoint)
    if r.response_code != 200:
        exit(1)