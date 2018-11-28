import json
from RestManager import RestManager

class PortfolioManager:

	label = "epita_group_7"
	code = "EUR"
	typef = "front"
	date = "2012-01-02"

	def buildJson(self, portfolio):
		assetList = []
		for pair in portfolio.assets:
			assetList.append({'asset': {'asset': pair[0], 'quantity': pair[1]}})
		return {'currency': {'code': self.code}, 'label': self.label, 'type': self.typef, 'values': {self.date: assetList}}

	def putPortfolio(self, body):
		api = RestManager()
		api.put('portfolio/1034/dyn_amount_compo', body)

class Portfolio:
	assets = []

	def addAsset(self, asset, quantity):
		self.assets.append((asset, quantity)) 

	def dump(self):
		for pair in self.assets:
			print(pair[0], ' : ', pair[1])
