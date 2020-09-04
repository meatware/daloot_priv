from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

Base = declarative_base()

engine = create_engine('sqlite:///pythonsqlite.db')

def init_db():
    """

    import all modules here that might define models so that
    they will be registered properly on the metadata.  Otherwise
    you will have to import them first before calling init_db()
    """

    from model import Item, Combo
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)
    # Use to 
    # inst = inspect(Item)
    # print([c_attr.key for c_attr in inst.mapper.column_attrs])


Session = sessionmaker(bind=engine)

# create a Session
session = Session()