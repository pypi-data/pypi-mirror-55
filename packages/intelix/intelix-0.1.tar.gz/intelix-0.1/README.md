# Sophos Labs Intelix
Client for the Sophos Labs Intelix API

https://api.labs.sophos.com/doc/index.html

## example

Connect to the API by providing your client ID and secret key 

```
import intelix
clientId = "xxxxxxxxxxx"
secret = "xxxxxxxxxxxxxxxxxxxxxxxxx"
url = "www.sophos.com"

i = intelix.client(clientId,secret)
i.url_lookup(url)
print(i.productivityCategory)
```



