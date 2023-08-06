'''
    Author: Randy Chang
    Synopsis: Fully featured and functional GraphQL Client Library for QA testing.  This is based on original Python GQL,
     which Rakuten engineer, Eran Kampf, is an author of.

    Todo as of 6/18/2019
    - Implement support to auto-convert file in the constructor
    - Implement support for GQL fragment import
    - Implement support for subscription
'''

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import inspect


# decorator to auto convert filepath to query string for graphql client
def convertfile(original_func):
    def func_wrapper(*args, **kwargs):
        def resolve_filename_to_string(query):
            query_string = None
            if ".graphql" in query or ".gql" in query:
                with open(query) as f:
                    query_string = f.read()

                if not query_string:
                    raise EOFError("GraphQL file is empty or invalid")
            else:
                query_string = query  # this is not a filename
            return query_string

        if "query_string" in kwargs:
            query_string = resolve_filename_to_string(kwargs["query_string"])
            kwargs["query_string"] = query_string
        else:
            query_string_index = inspect.getfullargspec(original_func).args.index("query_string")
            query_string = resolve_filename_to_string(args[query_string_index])
            args = [*args]
            args[query_string_index] = query_string
        return original_func(*args, **kwargs)

    return func_wrapper


class GraphQLClient():
    '''
        constructor function
        @param baseURL - the url of graphql route.  e.g. https://www.google.com/ebgraph
        @param doc - optional GQL document. Set for repeated use with parameters
    '''

    def __init__(self, baseURL: str, doc: str = None, headers: dict = None):
        self._url = baseURL

        _transport = RequestsHTTPTransport(
            url=self._url,
            use_json=True,
            headers=headers
        )
        client = Client(
            transport=_transport,
            fetch_schema_from_transport=True,
        )
        self._client = client
        self._document = doc

    @property
    def document(self):
        return self._document

    @property
    def client(self):
        return self._client

    @property
    def url(self):
        return self._url

    @document.setter
    def document(self, val):
        self._client.validate(val)
        self._document = val

    '''
        Query Function
        @param query_string - GQL document.  If not set, then client will use object internal document.
            However, if this argument is set, it will always override object internal document
        @param parameters - GQL parameters to use with the document
        @return - dictionary parsed from json response
    '''

    @convertfile
    def run(self, query_string: str, parameters: dict = None) -> dict:
        # use internal GQL document if query_string is empty
        # if query_string is not None, then it will always override object internal document
        if not query_string:
            query_string = self._document

        return self._client.execute(gql(query_string), variable_values=parameters)

    '''
        Validate Function
        @param query_string - GQL document to be validated.  This can be a full path to a .graphql or .gql file. 
            convertfile decorator will do the auto conversion
        @return function returns nothing.  If validation fails, then GraphQLError is raised
    '''

    @convertfile
    def validate(self, query_string: str) -> bool:
        return self._client.validate(gql(query_string))

        '''
        Static query method for single use.  Same functionality as run method
        @param url - GraphQL endpoint
        @param query_string - GQL document to be validated.  This can be a full path to a .graphql or .gql file.
                                convertfile decorator will do the auto conversion
        @param parameters - GQL parameters to use with the document
		function returns nothing.  If validation fails, then GraphQLError is raised
    '''

    @classmethod
    @convertfile
    def query(self, url, query_string: str, parameters: dict = None, headers: dict = None) -> dict:
        _transport = RequestsHTTPTransport(
            url=url,
            use_json=True,
            headers=headers
        )
        client = Client(
            transport=_transport,
            fetch_schema_from_transport=True,
        )

        return client.execute(gql(query_string), variable_values=parameters)


# Example usages
if __name__ == "__main__":
    query1 = """
	query campaignByNameQuery ($campaignName: String!, $start: Int, $rows: Int) {
	  result: campaignByName(name: $campaignName) {
	    id
	    name
	    urlName
	    description
	    ownerEntityId
	    pageTitle
	    start
	    expires
	    type
	    stores(pagination: {start: $start, rows: $rows}) {
	      pagination {
	        start
	        rows
	        total
	      }
	      storeList {
	      	...StoreProperties
	      }
	    }
	  }
	}

	fragment StoreProperties on Store {
		id
		name
		description
		urlName
		shoppingLink
		secrets
		link
		shoppingLink
		navId
		merchantOffersOnly
		couponCount
		cashBack {
			type
			amount
			baseAmount
			isRange
			currency {
				symbol
				code
			}
		}
	    images {
	        banner816x496
	    }
	    attributes {
	        iSCBMobileOrderIndex
	    }
	    campaignEntity {
	        id
	        shoppingLink
	        images {
	          adsGoogle
	        }
	        attributes {
	          navId
	        }
	    }
	}

	"""

    query2 = '''
	query {
	  result: campaignByName(name: "Cruises Sponsored Stores") {
	    id
	    name
	    urlName
	    description
	    ownerEntityId
	    pageTitle
	    start
	    expires
	    type
	  }
	}
	'''

    '''
    parameters = {
        "campaignName":"Cruises Sponsored Stores",
        "start": 0,
        "rows": 2
    }

    parameters2 = {
        "campaignName":"Homepage Featured Stores",
        "start": 0,
        "rows": 10
    }


    #Query using static method
    result = GraphQLClient.query("https://qa-www.ebates.com/ebgraph",query1,parameters)
    result = GraphQLClient.query("https://qa-www.ebates.com/ebgraph",query2)
    #result is in dictionary format, parsed from json 


    #Query using object.  Reusing same URL for multiple times
    client = GraphQLClient("https://qa-www.ebates.com/ebgraph")
    result = client.run(query1,parameters)
    result = client.run(query2)
    #result is in dictionary format, parsed from json 


    #Query using object.  Reusing same URL and same GQL document for multiple times
    client = GraphQLClient("https://qa-www.ebates.com/ebgraph",query1)
    result = client.run(parameters=parameters)
    result = client.run(parameters=parameters2)
    #result is in dictionary format, parsed from json 


    #Validate corretness of GQL document only.  NO ACTUAL QUERY
    client = GraphQLClient("https://qa-www.ebates.com/ebgraph")
    client.validate(query1)
    client.validate(query2)
    #if validation fails, then GraphQLError is raised
    '''

    query3 = '''
		query feed ($locale:Locale, $platform: ClientPlatform, $tenant: EbatesTenant, $slug: String!, $after: String, $before:String, $first: Int, $last: Int) {
  root(locale: $locale, platform: $platform, tenant: $tenant){
    feed(slug: $slug) {
      id
      slug
      event {
        name
        payload
      }
      topics(after: $after, before: $before, first: $first, last: $last) {
        totalCount
        pageInfo {
          endCursor
          hasNextPage
          hasPreviousPage
          startCursor
        }
        edges {
          cursor
          node {
            event {
              name
              payload
            }
            id
            title
          }
        }
      }
    }
  }
}	
'''

'''
param3 = {
  "locale":"en_US",
  "platform":"MOBILE",
  "tenant":"USA",
  "slug":"awesomeqawithnewbiedevtesting"
}	

#result = GraphQLClient.query("https://feedgen-qa1.nonprod.rakutenrewards-it.com/ebgraph",query3,param3,headers={"x-admin":"true"})
#result = GraphQLClient.query("https://feedgen-qa1.nonprod.rakutenrewards-it.com/ebgraph",query_string="/Users/rchang/Temp/feed1.graphql",parameters=param3,headers={"x-admin":"true"})
result = GraphQLClient.query("https://feedgen-qa1.nonprod.rakutenrewards-it.com/ebgraph","/Users/rchang/Temp/feed1.graphql",parameters=param3,headers={"x-admin":"true"})

print(result)
'''

