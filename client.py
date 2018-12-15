import requests

from constants import BASE_URL

class ReadingQuantifiedClient(object):
    """
    The client is responsible for making calls to the Reading Quantified Server APIs.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password

        # Request API tokens on init
        self.request_api_tokens()
        

    # Make this private?
    def request_api_tokens(self):
        """
        Retrieve the token pair (access & refresh) for a given user.
        """
        data = {
            'username': self.username,
            'password': self.password
        }

        r = requests.post(BASE_URL + '/api/token/', data=data)
        self.refresh_token = r.json()['refresh']
        self.access_token = r.json()['access']


    # Make this private?
    def request_new_access_token(self):
        """
        Retrieve a new access token if the refresh token is still valid.
        """
        data = {
            'refresh': self.refresh_token
        }

        r = requests.post(BASE_URL + '/api/token/refresh/', data=data)
        self.access_token = r.json()['access']


    def make_authorization_header(self):
        """
        Create the authorization header that's needed to make requests.
        """

        return {
            'Authorization' : 'Bearer %s' % self.access_token
        }


    def get(self, path):
        """
        Make a GET request.
        """
        try:
            r = requests.get(BASE_URL + path, headers=self.make_authorization_header())
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            return "Error: " + str(e)

        return r.json()


    def post(self, path, data):
        """
        Make a POST request.
        """
        try:
            r = requests.post(BASE_URL + path, data=data, headers=self.make_authorization_header())
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            return "Error: " + str(e)

        return r