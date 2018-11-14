from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbInit import Asset, Currency

class dbManager:
    
    session = None
    connection = None

    def __init__(self):
        engine = create_engine('sqlite:///database.sqlite', echo=True)
        self.connection = engine.connect()
        Session = sessionmaker(bind=engine)
        Session.configure(bind=engine)
        self.session = Session()

    def insertAsset(self, assetId, price, assetType, sharpe_ratio):
        asset = Asset(rest_id=assetId, close_value=price, asset_type=assetType, sharpe=sharpe_ratio)
        self.session.add(asset)
        assets = self.session.query(Asset).filter_by(rest_id=assetId)
        for asset in assets:
            print(asset)
        self.session.commit()

    def insertCurrency(self, curName, curValue):
        currency = Currency(name=curName, value=curValue)
        self.session.add(currency)
        currencies = self.session.query(Currency).filter_by(name=curName)
        for currency in currencies:
            print(currency)
        self.session.commit()
    
    def close(self):
        self.connection.close()