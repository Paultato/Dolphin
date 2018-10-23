import requests
from requests.auth import HTTPBasicAuth

class RestManager:

	URI = 'https://dolphin.jump-technology.com:3472'
	basePath = '/api/v1/'
	username = 'epita_user_7'
	pwd = 'td92D2UbcAyX2LZu'

	def get(self, path):
		response = requests.get(self.URI + self.basePath + path, auth=HTTPBasicAuth(self.username, self.pwd))
		return response.content