import requests
import time
x = time.time()
wallet_ID_Yogi = "0x3A5bd1E37b099aE3386D13947b6a90d97675e5e3"
id = "0x15"
data = {"profile_id": id}
URL = "http://127.0.0.1:5000/minimalens"

result = requests.post(URL, json=data   )
print(result.text)
print(time.time() - x)