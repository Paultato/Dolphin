import pandas
import json
from RestManager import RestManager
from dbManager import dbManager


class CorrelationManager:

    db = dbManager()
    api = RestManager()
    assets = []
    data = {}
    dataframe = None

    def __init__(self):
        db_assets = self.db.getAssets()
        for ass in db_assets:
            self.assets.append(ass.rest_id)
    
    def body(self, id):
        data = {"ratio" : [19], "asset" : self.assets, "benchmark" : id}
        return data
    
    def get_corr(self, id):
        response = self.api.post("ratio/invoke", self.body(id))
        res = json.loads(response)
        result = []
        for ass in self.assets:
            result.append(res[str(ass)][str(19)]['value'])
        return result

    def build_data(self):
        for ass in self.assets:
            self.data[ass] = self.get_corr(ass)
    
    def build_csv(self):
        self.build_data()
        doc = {'id': self.assets}
        for ass in self.assets:
            doc[ass] = self.data[ass]
        df = pandas.DataFrame(doc)
        print(df)
        df.to_csv('corr.csv', sep=',', index=False)

    def build_df(self):
        df = pandas.read_csv('corr.csv', sep=',')
        df.set_index('id', inplace=True)
        self.dataframe = df

    def value(self, i, j):
        return self.dataframe[str(i)][j]

cm = CorrelationManager()
#cm.build_csv()
#print(cm.dataframe)
cm.build_df()
print(cm.dataframe)
print(cm.value(1001, 717))