class BookEndpoints(object):
    """
    Class for accessing the book API endpoints.
    """

    path = '/api/books/'

    def __init__(self, client):
        self.client = client


    def get_books(self, query_params={}):
        return self.client.get(self.path, query_params=query_params)

    
    def get_book_by_id(self, id):
        return self.client.get(self.path + str(id))


    def post_book(self, book):
        return self.client.post(self.path, book.to_json())

    def put_book(self, url, book):
        """
        Update book with a PUT request. Note: URL with ID must be specified.
        """
        return self.client.put(url, book.to_json())


class GenreEndpoints(object):
    """
    Class for accessing the genre API endpoints.
    """

    path = '/api/genres/'

    def __init__(self, client):
        self.client = client

    def get_genres(self):
        return self.client.get(self.path)

    def post_genre(self, genre):
        return self.client.post(self.path, genre.to_json())