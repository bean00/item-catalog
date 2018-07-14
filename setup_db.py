from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, Category, Item

engine = create_engine('postgresql://vagrant:word@localhost/itemcatalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

