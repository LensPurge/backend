import json
import os

class LensCacher(object):

    FILEPATH = "home/pbbecker/backend/bigquery/py/cache.json"
    FILEPATH = r"C:\Users\Demo\git\eth_global\backend\bigquery\py\cache.json"

    def __init__(self):
        self.create_json()
       

    def add_log(self,data, id, timestamp):
        key = str(id) + str(timestamp)
        json_data = self.get_json()
        if key not in json_data:
            json_data[key] = data

            self.dump_to_json(json_data)
      
    def is_saved(self, id, timestamp):
        key = str(id) + str(timestamp)

        json_data = self.get_json()
        if key in json_data:
            return True
        return False
     

    def get_saved(self, id, timestamp):
        key = str(id) + str(timestamp)
        json_data = self.get_json()

        if key not in json_data:
            raise ValueError(f"Key not in storage. Key: {key}")

        return json_data[key]

    def create_json(self):
        if not os.path.isfile(self.FILEPATH):
            os.makedirs(os.path.dirname(self.FILEPATH),exist_ok = True)
            self.dump_to_json({"test":"hi"})
                    
            

    def dump_to_json(self, data):
        with open(self.FILEPATH, "w") as outfile:
            json.dump(data, outfile)

    def get_json(self):
        with open(self.FILEPATH, "r") as outfile:
            return json.load(outfile)
       
