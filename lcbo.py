import urllib2
import json
from pprint import pprint

# my auth token. 
# Get yours at lcboapi.com
from token import mytoken

req = urllib2.Request('https://lcboapi.com/products')
token_string = "Token %s" % mytoken
req.add_header('Authorization', token_string)

data = json.load(urllib2.urlopen(req))

pprint(data)
