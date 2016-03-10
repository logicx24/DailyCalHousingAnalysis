"""
This program requires the Python oauth2 library, which you can install via:
`pip install -r requirements.txt`.
Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
import argparse
import json
import pprint
import sys
import urllib
import urllib2
import oauth2
import requests


API_HOST = 'api.yelp.com'
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = 'FmI5xWeT7qEqfRRrPRL8tQ'
CONSUMER_SECRET = 'JGOdZj4uRtlzp3NMjId6VurcWBw'
TOKEN = 'MeIvaQLkMa51m70HLpQw7OhxKBGc1F87'
TOKEN_SECRET = '9ChRhFEPoZB0F-sMrdhwbJpSVz0'


""" Prepares OAuth authentication and sends the request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
"""
def request(host, path, url_params=None):

    url_params = url_params or {}
    url = 'https://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(
        method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(
        oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url() # the url to put online

    print u'Querying {0} ...'.format(url)
    print signed_url
    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response


""" Query the Search API by a search term and location.
    Returns:
        dict: The JSON response from the request.
"""
def search(term = None, limit = None, offset = None, r = None, ll = None, location = None, bounds = None):
    url_params = {}
    if offset != None:
        url_params['offset'] = offset
    if term != None:
        url_params['term'] = term.replace(' ', '+')
    if limit != None:
        url_params['limit'] = limit   
    if r != None:
        url_params['radius_filter'] = r
    if ll != None:
        url_params['ll'] = ll.replace(' ', '+')
    if bounds != None:
        url_params['bounds'] = bounds
    if location != None:
        url_params['location'] = location.replace(' ', '+'),
    
    return request(API_HOST, SEARCH_PATH, url_params=url_params)


"""Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
"""
def get_business(business_id):
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path)



"""Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
"""
def query_api(term, location):
    response = search(term, location)
    businesses = response.get('businesses')

    if not businesses:
        print u'No businesses for {0} in {1} found.'.format(term, location)
        return

    business_id = businesses[0]['id']

    print u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id)
    response = get_business(business_id)

    print u'Result for business "{0}" found:'.format(business_id)
    pprint.pprint(response, indent=2)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.location)
    except urllib2.HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0}. Abort program.'.format(error.code))


if __name__ == '__main__':
    main()