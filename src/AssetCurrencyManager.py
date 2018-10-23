import json
import requests
from requests.auth import HTTPBasicAuth

class AssetCurrencyManager:

	refCurrency = "EUR"
	currencies = ["EUR", "USD", "GBp", "JPY", "NOK", "SEK"]
	changeRate = {}

	def __init__(self):
	
		for cur in currencies:
			req = requests.get('https://dolphin.jump-technology.com:3472/api/v1/currency/rate/' + refCurrency + '/to/' + cur, auth=HTTPBasicAuth('epita_user_7', 'td92D2UbcAyX2LZu'))
			res = json.loads(req.content)
			self.changeRate[cur] = res['rate']['value']

	def updateChangeRate():

		for cur in currencies:
			req = requests.get('https://dolphin.jump-technology.com:3472/api/v1/currency/rate/' + refCurrency + '/to/' + cur, auth=HTTPBasicAuth('epita_user_7', 'td92D2UbcAyX2LZu'))
			res = json.loads(req.content)
			self.changeRate[cur] = res['rate']['value']