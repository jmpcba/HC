from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from common import RDSConfig


if __name__ == '__MAIN__':
    Base = declarative_base()
    engine = create_engine(RDSConfig.ENGINE)
    Base.metadata.create_all()
