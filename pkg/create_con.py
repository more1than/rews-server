from sqlalchemy.orm import sessionmaker
from pkg.create_engine import create_myengine


def create_con():
    engine = create_myengine()
    Connection = sessionmaker(bind=engine)
    con = Connection()
    return con
