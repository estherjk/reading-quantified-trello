class Book(object):
    """
    Class representing a Book object.
    """
    def __init__(self, title, trello_id, date_started, date_finished, genres=[]):
        self.title = title
        self.trello_id = trello_id
        self.date_started = date_started
        self.date_finished = date_finished

        # This should be an array of trello label IDs
        self.genres = genres
        

    def to_json(self):
        return {
            'title': self.title,
            'trello_id': self.trello_id,
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


class Genre(object):
    """
    Class representing a Genre object.
    """
    def __init__(self, name, trello_id):
        self.name = name
        self.trello_id = trello_id

    def to_json(self):
        return {
            'name': self.name,
            'trello_id': self.trello_id
        }


class GenreEndpoints(object):
    """
    Class for accessing the genre API endpoints.
    """

    path = '/api/genres/'

    def __init__(self, client):
        self.client = client

    def post_genre(self, genre):
        return self.client.post(self.path, genre.to_json())