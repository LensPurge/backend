import requests

 
url = "https://api-mumbai.lens.dev/"

ADDR = "0xC8AbE11C25d5a804671bD77463f8be62c419a656"

 
body = """query Challenge {
  challenge(request: { address: "0xC8AbE11C25d5a804671bD77463f8be62c419a656" }) {
    text
  }
}
"""
 
response = requests.post(url=url, json={"query": body})
print("response status code: ", response.status_code)
if response.status_code == 200:
    print("response : ", response.content)