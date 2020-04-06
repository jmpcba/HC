from sqlalchemy.ext.declarative import declarative_base
import argparse
import logging
import models


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='DB setup options')
    parser.add_argument('operation', help='what operation do you want to execute?', choices=['setup',])
    args = parser.parse_args()

    if args.operation == 'setup':
        models.create_tables()
