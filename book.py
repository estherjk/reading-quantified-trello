class Book(object):
    """
    Class representing a Book object.
    """
    def __init__(self, title, date_started, date_finished, genres=[]):
        self.title = title
        self.date_started = date_started
        self.date_finished = date_finished
        self.genres = genres
        

    def to_json(self):
        return {
            'title': self.title,
            'date_started': self.date_started,
            'date_finished': self.date_finished,
            'genres': self.genres
        }
        

class BookEndpoints(object):
    """
    Class for accessing the book API endpoints.
    """

    path = '/api/books/'

    def __init__(self, client):
        self.client = client


    def get_books(self):
        return self.client.get(self.path)

    
    def get_book_by_id(self, id):
        return self.client.get(self.path + str(id))


    def post_book(self, book):
        return self.client.post(self.path, book.to_json())
