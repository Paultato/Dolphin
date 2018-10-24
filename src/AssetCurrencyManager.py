import json
from RestManager import RestManager

class AssetCurrencyManager:

	refCurrency = "EUR"
	currencies = ["EUR", "USD", "GBP", "JPY", "NOK", "SEK"]
	changeRate = {}

	def __init__(self):
		api = RestManager()
		for cur in self.currencies:
			response = api.get('currency/rate/' + self.refCurrency + '/to/' + cur)
			res = json.loads(response)
			self.changeRate[cur] = res['rate']['value']
		print(self.changeRate)