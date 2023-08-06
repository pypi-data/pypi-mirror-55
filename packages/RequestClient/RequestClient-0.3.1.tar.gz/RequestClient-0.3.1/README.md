##  Request Client 
An easy-to-use and convenient Python3 library for HTTP REST API request and GraphQL request.
This library is a wrapper around Python request library and the original GQL library.   

Currently supports Rest API method:
- Get
- Post
- Delete

NOTE: KeepAlive and Connection Pool is ON by default for Rest Client.  As the wrapper uses request session object to initiate request.

Future improvements:
- Support Rest Put and Patch
- Add documentations

## Sponsor
[logo]: https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Rakuten_Global_Brand_Logo.svg/2880px-Rakuten_Global_Brand_Logo.svg.png
Rakuten USA - CBSP@Rakuten Rewards

## Python3 (Install)  
Requirements:
- Python3 (version 3.7 or above)
- Pip3
```bash
pip3 install RequestClient
````

## Usage (Python3)
```python
from RequestClient.RestRequestClient import RestRequestClient, ResponseError
#For Rest API Client - transaction in JSON, 
# Content-negotiations and XML format NOT supported

from RequestClient.GraphQLClient import GraphQLClient
#For GraphQL Client

from unittest import TestCase

baseURL = "https://www.google.com"    #change this to your own for testing

client = RestRequestClient(baseUrl=baseURL,sslverify=False,defaultHeaders={"x-admin":"true"}, defaultAuth={"username":"password"}, defaultCookies={"token":"123"}, raiseExceptionOnStatusCode=True)
# baseUrl = the base URL accompanying every request.  e.g. https://www.google.com is the base URL for https://www.google.com/apis/v3/doc/123
# sslverify = verify SSL certificate?  if this is true, exception is raised on invalid SSL cert
# defaultHeaders = the headers accompanying every request
# defaultAuth = the base64 HTTP basic authorization accompanying every request
# defaultCookies = the cookies accompanying every request 
# raiseExceptionOnStatusCode = if true, then ResponseError will be raised for 4xx and 5xx response code

try:
    response = client.get("/apis/v3/doc")
    #this will issue GET request to "https://www.google.com/apis/v3/doc"

    print(response.content)     #get the dictionary content, parsed from JSON response
    #content is automatically parsed as Python dictionay if content is JSON
    #content is string if content isn't a valid JSON
    #we can check response type by response.type, it can be "JSON" or "RAW"
    print(response.status_code) #get the integer status code


    response = client.get("/store/list", params={"id":"98"})
    # params is the URL parameters being send 
    #e.g. params = {"x": 10, "y": 5, "z": 7} 
    # for https://www.google.com/apis/v3/doc?x=10&y=5&z=7    

    store98 = response.content   
    TestCase.assertTrue(store98["stores"]["store"][0]["id"] == 98 , "GET Test Failed")

    store45 = client.get("/store/45", additionalHeaders={"x-token":"123"}, params={"x":"1"}, cookies={"session":"123"}, auth={"username":"password"})
    # additionalHeaders will be combined with defaultHeaders and send with request
    # cookies here will be combined with cookie declared in constructor
    # auth here will replace the default auth in the constructor
    
    store45 = store45.object()
    # .object() exports response content into Python object
    # NOTE: the difference between response.content and response.object() 
    #       is that response.content is Python Dictionary
    #       and response.object() is Python Object.
    # e.g.  
    #   response = {"data": {"x":"1", "nest": {"y":"2"} } }
    # 
    # Access Python Dictionary: response,content["data"]["nest"]["y"]
    # Access Python Object:  res = response.object()
    #                        res.data.nest.y
    # .object() allows for JavaScript style dot access to response payload 
    #
    # Object is converted from Dictionary.  If response content isn't a valid JSON,
    #  then calling .object() will raise ResponseConversionError
    #
    # WARN: 1 .object() is experimental, use at your own risk.  
    #       2 .object() will strip non-alphanumeric characters out of property name
    #          e.g. data["@href"] will become data.href with @ stripped out
    TestCase.assertTrue(store45.store[0].id == 45, "Object Conversion test failed")

    category2 = client.post("/category/2", payload={"category": {"name":"Testing123", "modifiedBy":"Randy"}})
    #payload is the POST data to send to endpoint

    print(category2.type)   #will return and print "JSON" string
    TestCase.assertEqual(category2.content["category"][0]["name"], "Testing123", "Post Raw Python Dictionary Failed")

    
    category5 = client.get("/category/5")
    category5 = category5.object()
    TestCase.assertTrue(category5.category[0].status == "Published", "Object Conversion test failed")

except ResponseError as err:
    print(f"Oops, something is wrong here: {err}")


print("Yah! All tests pass!")
```

    
    

