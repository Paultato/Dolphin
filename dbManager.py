from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.sqlite', echo=True)
connection = engine.connect()
if not database_exists(engine.url):
    create_database(engine.url)
print(database_exists(engine.url))

Base = declarative_base()

class Currencies(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, Sequence('currencies_id_seq'), primary_key=True)
    name = Column(String)
    value = Column(Integer)

    def __repr__(self):
        return "<Currency(name='%s', value='%s')>" % (self.name, self.value)

Currencies.__table__
Base.metadata.create_all(engine)

connection.close()