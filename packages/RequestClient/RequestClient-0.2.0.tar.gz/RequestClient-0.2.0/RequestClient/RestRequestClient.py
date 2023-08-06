'''
    Author: Randy Chang
    Synopsis: Fully featured and functional HTTP Request Client Wrapper Library.

    Todo as of 11/04/2019
    - Add GraphQL Request Client

'''

import requests
import pydash
import re
from collections import namedtuple

class ResponseConvertionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

class Response():
    def __init__(self, response):
        #this will ensure contents are always read, and thus connection can be re-used at the pool
        self.status_code = response.status_code

        try:
            self.content = response.json()
            self.type = "JSON"
        except:
            self.content = response.content
            self.type = "RAW"

    def _convertDictionaryToObject(self, name, dictionary):
        name =  re.sub(r"[^\w]","",name)    #strip name of non-alphanumeric characters
        name = "random" if name == "" else name #assign "random" as name if name is empty after strip
        if (type(dictionary) == dict):
            invalid_name_for_deletion = []
            new_names = {}
            for item in dictionary:
                if type(dictionary[item]) == dict or type(dictionary[item]) == list:
                    dictionary[item] = self._convertDictionaryToObject(item, dictionary[item])
                # strip name of non-alphanumeric characters
                if re.match(r"[^\w]", item):
                    new_name = re.sub(r"[^\w]", "", item)
                    new_name = "random" if item == "" else new_name
                    new_names[new_name] = dictionary[item]
                    invalid_name_for_deletion.append(item)

            if len(invalid_name_for_deletion) > 0:
                for item in invalid_name_for_deletion:
                    del dictionary[item]
                pydash.merge(dictionary, new_names)

            return namedtuple(name, dictionary.keys())(*dictionary.values())
        else:  # this is actually a list
            for index, item in enumerate(dictionary):
                if type(item) == dict or type(item) == list:
                    dictionary[index] = self._convertDictionaryToObject(name, item)
            return dictionary

    def object(self):
        if self.type != "JSON":
            raise ResponseConvertionError(f"Response Content is NOT JSON, cannot be converted to Object!")
        return self._convertDictionaryToObject("Response", self.content)


class ResponseError(Exception):
    def __init__(self, code, content):
        self.code = code
        self.content = content
        super().__init__(f"HTTP Response Error! Code {code}: {content}")

    def __str__(self):
        return f"HTTP Response Error! Code {self.code}: {self.content}"

    def __repr__(self):
        return f"HTTP Response Error! Code {self.code}: {self.content}"

class RestRequestClient():
    def __init__(self, baseUrl, sslverify=True, defaultHeaders = {}, defaultAuth=None, defaultCookies={}, raiseExceptionOnStatusCode=True):
        self.session = requests.Session()
        self.baseUrl = baseUrl
        self.sslverify = sslverify
        self.raiseException = raiseExceptionOnStatusCode

        self.session.headers.update(defaultHeaders)
        self.session.cookies.update(defaultCookies)
        if defaultAuth:
            self.session.auth = defaultAuth

    # @Function: Post Request using json payload via app server
    # @param api:   the api routes after base uri
    # @param payload: json payload.  Typically Python dictionary with json.dumps()
    # @Return:  raw response object
    def _send_x_post(self, api, payload, headers, params, cookies, auth):
        parameters = {
            "url": re.sub(r"(?<!:)/+", "/", f"{self.baseUrl}/{api}"),   #remove duplicate /
            "headers": headers,
            "cookies": cookies,
            "verify": self.sslverify,
            "params": params
        }
        if type(payload) == dict:
            parameters["json"] = payload
        else:
            parameters["data"] = payload

        if auth:
            parameters["auth"] = auth

        response = self.session.post(**parameters)
        return response

    # @Function: Get Request via app server
    # @param api:   the api routes after base uri
    # @Return:  Raw response object
    def _send_x_get(self, api, headers, params, cookies, auth):
        parameters = {
            "url": re.sub(r"(?<!:)/+", "/", f"{self.baseUrl}/{api}"),
            "headers": headers,
            "cookies": cookies,
            "verify": self.sslverify,
            "params": params
        }
        if auth:
            parameters["auth"] = auth

        response = requests.get(**parameters)
        return response

    # @Function: Delete Request via app server
    # @param api:   the api routes after base uri
    # @Return:  Raw response object
    def _send_x_delete(self, api, headers, params, cookies, auth):
        parameters = {
            "url": re.sub(r"(?<!:)/+", "/", f"{self.baseUrl}/{api}"),
            "headers": headers,
            "cookies": cookies,
            "verify": self.sslverify,
            "params": params
        }
        if auth:
            parameters["auth"] = auth

        response = requests.delete(**parameters)
        return response

    def _check_response(self, res):
        if self.raiseException and int(res.status_code) >= 400:
            raise ResponseError(res.status_code, res.content)

    # @Function: Post Request using json payload
    # @param api:   the api routes after CBSP partner ID (e.g. /inquiry/reward/calculator)
    # @param payload: json payload.  Typically Python dictionary with json.dumps()
    # @Return:  raw response object
    def post(self, api, payload, additionalHeaders={}, params={}, cookies={}, auth=None):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        pydash.merge(headers, additionalHeaders)
        response = self._send_x_post(api, payload, headers, params, cookies, auth)
        self._check_response(response)
        return Response(response)

    # @Function:Get Request for json payload
    # @param api:   the api routes after base uri
    # @Return:  Raw response object
    def get(self, api, additionalHeaders={}, params={}, cookies={}, auth=None):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        pydash.merge(headers, additionalHeaders)
        response = self._send_x_get(api, headers, params, cookies, auth)
        self._check_response(response)
        return Response(response)

    # @Function: X-Admin Delete Request, json payloads
    # @param api:   the api routes after base uri
    # @Return:  Raw response object
    def delete(self, api, additionalHeaders={}, params={}, cookies={}, auth=None):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        pydash.merge(headers, additionalHeaders)
        response = self._send_x_delete(api, headers, params, cookies, auth)
        self._check_response(response)
        return Response(response)
