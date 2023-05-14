# Backend

Backend for ETH-Global Lisbon 2023. <br>

Webservice, which queues data from Lens-BigQuery.<br>

Takes wallet-address as input, queues all associated interactions including: 
-   collections
-   comments
-   reactions
-   mirrors of comments
-   mirrors of posts

<br>
With these interactions, profiles which are not relevant for the user are identified. For these user, following information are collected:

-   img_link
-   handle
-   name
-   nft_addr

# Usage
The webservice is deployed to a pythonanywhere.com space.<br>
You can reach the endpoint at:<br>

```
https://pbbecker.pythonanywhere.com/minimalens
```

You have to POST the endpoint with the following json, replacing "id" with your wallet_id :<br>

```
{"profile_id": id}
```
