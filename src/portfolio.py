import json

class PortfolioManager:

	label = "epita_group_7"
	code = "EUR"
	typef = "front"
	date = "2012-01-02"

	def buildJson(self, assets):
		assetList = []
		for pair in assets:
			assetList.append({'asset': {'asset': pair[0], 'quantity': pair[1]}})
		print(assets)
		print(assetList)
		return {'currency': {'code': self.code}, 'label': self.label, 'type': self.typef, 'values': {self.date: assetList}}

class Portfolio:
	assets

	def addAsset(self, asset, quantity):
		asset.append((asset, quantity))

	def dump(self):
		for pair in self.assets:
			print(pair[0], ' : ', pair[1])


