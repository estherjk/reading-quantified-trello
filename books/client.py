import requests

class ReadingQuantifiedClient:
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


    def get(self, url, query_params={}):
        """
        Make a GET request.
        """
        try:
            r = requests.get(url, headers=self.make_authorization_header(), params=query_params)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            return "Error: " + str(e)

        return r.json()


    def post(self, url, data):
        """
        Make a POST request.
        """
        try:
            r = requests.post(url, data=data, headers=self.make_authorization_header())
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            return "Error: " + str(e)

        return r

    def put(self, url, data):
        """
        Make a PUT request.
        """
        try:
            r = requests.put(url, data=data, headers=self.make_authorization_header())
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            return "Error: " + str(e)

        return r

    def get_books(self, query_params={}):
        """
        Return all books on the Reading Quantified Server.
        """
        return self.get(self.base_url + '/api/books/', query_params=query_params)

    def add_book(self, book):
        """
        Add a book to the Reading Quantified Server.
        """
        return self.post(self.base_url + '/api/books/', book.to_json())

    def update_book(self, url, book):
        """
        Update an existing book on the Reading Quantified Server.
        Note: The server uses an `url` field instead of the primary key field to represent relationships. Pass the URL instead of an ID.
        """
        return self.put(url, book.to_json())

    def get_genres(self, query_params={}):
        """
        Return all genres on the Reading Quantified Server.
        """
        return self.get(self.base_url + '/api/genres/', query_params=query_params)

    def add_genre(self, genre):
        """
        Add a genre to the Reading Quantified Server.
        """
        return self.post(self.base_url + '/api/genres/', genre.to_json())