from sqlalchemy import create_engine, Column, Integer, String, Sequence, Float, Numeric
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
engine = create_engine('sqlite:///database.sqlite', echo=True)
connection = engine.connect()
if not database_exists(engine.url):
    create_database(engine.url)
print("Database Existing: ", database_exists(engine.url))
 
Base = declarative_base()
 
class Currency(Base):
    __tablename__ = 'currency'

    id = Column(Integer, Sequence('currency_id_seq'), primary_key=True)
    name = Column(String)
    value = Column(Float)

    def __repr__(self):
        return "<Currency(name='%s', value='%f')>" % (self.name, self.value)

class Asset(Base):
    __tablename__ = 'asset'

    id = Column(Integer, Sequence('asset_id_seq'), primary_key=True)
    rest_id = Column(Integer)
    close_value = Column(Integer)
    close_value_decimal = Column(Integer)
    asset_type = Column(String)
    sharpe = Column(Numeric(precision=15))

    def __repr__(self):
        return "<Asset(REST ID='%d', Close Value='%d', Close Value Decimal='%d', Type='%s', Sharpe='%f')>" % (self.rest_id, self.close_value, self.close_value_decimal, self.asset_type, self.sharpe)
 

Currency.__table__
Asset.__table__
Base.metadata.create_all(engine)
 
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()
session.commit()
 
connection.close()