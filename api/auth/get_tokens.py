import requests

 
url = "https://api-mumbai.lens.dev/"

ADDR = "0xC8AbE11C25d5a804671bD77463f8be62c419a656"
PRIVATE = "747f242e355e2a948f856ad2cc1abe1a2c34ba150e4bebc2b0907ddeaca90e9f"
 
body = """mutation Authenticate {
  authenticate(request: {
    address: "0xC8AbE11C25d5a804671bD77463f8be62c419a656",
    signature: "747f242e355e2a948f856ad2cc1abe1a2c34ba150e4bebc2b0907ddeaca90e9f"
  }) {
    accessToken
    refreshToken
  }
}
"""
 
response = requests.post(url=url, json={"query": body})
print("response status code: ", response.status_code)
if response.status_code == 200:
    print("response : ", response.content)