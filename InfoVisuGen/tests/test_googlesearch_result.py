"""
    script: test_googlesearch_result.py 
    description: check that the Google Search API returns a response when request is sent
"""

import requests 
import googlesearch as gsearch

def test_request_response():
    # sends request to the API server, store the response
    response = requests.get('http://....')

    # confirms that the request-reponse cycle completed successfully 
    asset_true(response.ok)
