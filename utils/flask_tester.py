import requests
import time
x = time.time()
wallet_ID_Yogi = "0x3A5bd1E37b099aE3386D13947b6a90d97675e5e3"
id = "0xC8AbE11C25d5a804671bD77463f8be62c419a656"
id = "0x9b62f67D0E2677d40D93e59EAA0eC828C915dCCf"
data = {"profile_id": id}
#URL = "https://pbbecker.pythonanywhere.com/minimalens"
URL = "http://127.0.0.1:5000/minimalens"

result = requests.post(URL, json=data)
print(result.text)
print(time.time() - x)