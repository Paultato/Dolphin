from dbManager import dbManager
import json
from RestManager import RestManager
from currencyManager import AssetCurrencyManager

def getAssets():
	api = RestManager()
	db = dbManager()
	response = api.get('asset')
	assets = json.loads(response)
	acm = AssetCurrencyManager()

	for asset in assets:
		assetId = int(asset["REST_OBJECT_ID"]["value"])
		price = getPrice(asset["LAST_CLOSE_VALUE"]["value"], acm.changeRate, asset["CURRENCY"]["value"])
		sharpe = getSharpe(assetId)
		db.insertAsset(assetId, price, asset["TYPE"]["value"], sharpe)


def getPrice(price_str, changeRate, currency):
	price_str = price_str.replace(',', '.')
	price_str = price_str.split(' ', 1)[0]
	price = float(price_str)
	print(float(changeRate[currency]))
	print('price = ' + str(price))
	price *= float(changeRate[currency])
	print('price = ' + str(price))
	return price

def getSharpe(assetId):
	data = {"ratio": [20], "asset": [assetId]}
	api = RestManager()
	response = api.post("ratio/invoke", data)
	res = json.loads(response)
	return float((res[str(assetId)]["20"]["value"]).replace(',', '.'))

getAssets()