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

    def getAssets(self):
        return self.session.query(Asset)

    def getCurrencies(self):
        return self.session.query(Currency)

    def insertAsset(self, assetId, price, price_decimal, assetType, sharpe_ratio):
        asset = Asset(rest_id=assetId, close_value=price, close_value_decimal=price_decimal, asset_type=assetType, sharpe=sharpe_ratio)
        exists = self.session.query(Asset).filter_by(rest_id=assetId).first() is not None
        print(exists)
        if not exists:
            self.session.add(asset)
        else:
            print("Asset already in the database")
        self.session.commit()

    def insertCurrency(self, curName, curValue):
        currency = Currency(name=curName, value=curValue)
        self.session.add(currency)
        self.session.commit()
    
    def close(self):
        self.connection.close()