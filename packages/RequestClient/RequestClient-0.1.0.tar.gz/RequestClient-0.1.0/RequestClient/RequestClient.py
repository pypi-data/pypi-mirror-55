'''
    Author: Randy Chang
    Synopsis: Fully featured and functional HTTP Request Client Wrapper Library.

    Todo as of 11/04/2019
    - Add GraphQL Request Client

'''

import requests
import json
import pydash

class Response():
    def __init__(self, response):
        self.status_code = response.status_code
        self.content = json.loads(response.content)

class RestRequestClient():
    def __init__(self, baseUrl, verify=False, defaultHeaders = {}):
        self.baseUrl = baseUrl
        self.verify = verify
        self.defaultHeaders = defaultHeaders

    # @Function: Post Request using json payload via app server
    # @param api:   the api routes after base uri
    # @param payload: json payload.  Typically Python dictionary with json.dumps()
    # @Return:  raw response object
    def send_x_post(self, api, payload, headers={}):
        pydash.merge(headers, self.defaultHeaders)
        url = f"{self.baseUrl}/{api}"
        response = requests.post(url,data=payload,headers=headers,verify=self.verify)
        return response

    # @Function: Get Request via app server
    # @param api:   the api routes after base uri
    # @Return:  Raw response object
    def send_x_get(self, api, headers={}):
        pydash.merge(headers, self.defaultHeaders)
        url = f"{self.baseUrl}/{api}"
        response = requests.get(url,headers=headers,verify=self.verify)
        return response

    # @Function: Delete Request via app server
    # @param api:   the api routes after base uri
    # @Return:  Raw response object
    def send_x_delete(self, api, headers={}):
        pydash.merge(headers, self.defaultHeaders)
        url = f"{self.baseUrl}/{api}"
        response = requests.delete(url, headers=headers, verify=self.verify)
        return response

    # @Function: Post Request using json payload
    # @param api:   the api routes after CBSP partner ID (e.g. /inquiry/reward/calculator)
    # @param payload: json payload.  Typically Python dictionary with json.dumps()
    # @Return:  raw response object
    def post(self, api, payload, additionalHeaders={}):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        pydash.merge(headers, additionalHeaders)
        response = self.send_x_post(api,json.dumps(payload), headers)
        return Response(response)

    # @Function:Get Request for json payload
    # @param api:   the api routes after base uri
    # @Return:  Raw response object
    def get(self, api, additionalHeaders={}):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        pydash.merge(headers, additionalHeaders)
        response = self.send_x_get(api, headers)
        return Response(response)

    # @Function: X-Admin Delete Request, json payloads
    # @param api:   the api routes after base uri
    # @Return:  Raw response object
    def delete(self, api, additionalHeaders={}):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        pydash.merge(headers, additionalHeaders)
        response = self.send_x_delete(api, headers)
        return Response(response)
