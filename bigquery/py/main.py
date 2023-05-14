from utils.big_query_handler import BigQueryHandler
from flask import Flask, jsonify, request
import json


timestamp = "2023-05-01 09:00:00"


handler = BigQueryHandler()
app = Flask(__name__)


    
#{"profile_id":"12345"}
@app.route('/minimalens', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    if "profile_id" not in record:
        return "'profile_id' not found in data you transmitted", 400
    profile_id =record["profile_id"]
    easy_kills = handler.run(profile_id, timestamp)
    return jsonify(easy_kills)

#app.run()

