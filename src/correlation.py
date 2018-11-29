import pandas
import json
from RestManager import RestManager
from dbManager import dbManager


class CorrelationManager:

    db = dbManager()
    api = RestManager()
    assets = []

    def __init__(self):
        db_assets = self.db.getAssets()
        for ass in db_assets:
            self.assets.append(ass.rest_id)
        print(self.assets)
    
    def body(self, id):
        data = {"ratio" : [19], "asset" : self.assets, "benchmark" : id}
        print(data)
        return data
    
    def get_corr(self, id):
        response = self.api.post("ratio/invoke", self.body(id))
        res = json.loads(response)
        print(res)
        return res

cm = CorrelationManager()
cm.body(597)