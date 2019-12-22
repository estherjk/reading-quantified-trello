import requests

class ReadingQuantifiedClient(object):
    """
    The client is responsible for making calls to the Reading Quantified Server APIs.
    """

    def __init__(self, base_url, username, password):
        self.base_url = base_url
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

        r = requests.post(self.base_url + '/api/token/', data=data)
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

        r = requests.post(self.base_url + '/api/token/refresh/', data=data)
        self.access_token = r.json()['access']


    def make_authorization_header(self):
        """
        Create the authorization header that's needed to make requests.
        """

        return {
            'Authorization' : 'Bearer %s' % self.access_token
        }


    def get(self, path, query_params={}):
        """
        Make a GET request.
        """
        try:
            r = requests.get(self.base_url + path, headers=self.make_authorization_header(), params=query_params)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            return "Error: " + str(e)

        return r.json()


    def post(self, path, data):
        """
        Make a POST request.
        """
        try:
            r = requests.post(self.base_url + path, data=data, headers=self.make_authorization_header())
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            return "Error: " + str(e)

        return r

    def put(self, url, data, custom_url=None):
        """
        Make a PUT request. An URL instead of a path must be specifiedd.
        """
        try:
            r = requests.put(url, data=data, headers=self.make_authorization_header())
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            return "Error: " + str(e)

        return r