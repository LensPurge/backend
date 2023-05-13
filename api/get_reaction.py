import requests

 
url = "https://testnet.lenster.xyz/"

ADDR = "0xC8AbE11C25d5a804671bD77463f8be62c419a656"

 
body = """uery Publications {
  publications(request: {
    profileId: "0x09",
    publicationTypes: [POST, COMMENT, MIRROR],
    limit: 10,
  }) {
    items {
      __typename 
      ... on Post {
        reaction(request: { profileId: "0x01" })
      }
      ... on Comment {
        reaction(request: { profileId: "0x01" })
      }
      ... on Mirror {
        reaction(request: { profileId: "0x01" })
      }
    }
    pageInfo {
      prev
      next
      totalCount
    }
  }
}
"""
 
response = requests.post(url=url, json={"query": body})
print("response status code: ", response.status_code)
if response.status_code == 200:
    print("response : ", response.content)