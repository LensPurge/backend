import requests
from query import QUERY
 
url = "https://api-mumbai.lens.dev/"
 
body = QUERY
 
response = requests.post(url=url, json={"query": body})
print("response status code: ", response.status_code)
if response.status_code == 200:
    print("response : ", response.content)