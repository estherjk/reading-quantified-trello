import json

class Book:
    """
    Class representing a Book object.
    """
    def __init__(self, title, trello_id, date_started, date_finished, genres=[], cover_attachment={}):
        self.title = title
        self.trello_id = trello_id
        self.date_started = date_started
        self.date_finished = date_finished

        # This should be an array of trello label IDs
        self.genres = genres

        # This should be a card's cover attachment info
        self.cover_attachment = cover_attachment

    def to_json(self):
        return {
            'title': self.title,
            'trello_id': self.trello_id,
            'date_started': self.date_started,
            'date_finished': self.date_finished,
            'genres': self.genres,
            'cover_attachment': json.dumps(self.cover_attachment)
        }


class Genre:
    """
    Class representing a Genre object.
    """
    def __init__(self, name, trello_id, color=''):
        self.name = name
        self.trello_id = trello_id
        self.color = color

    def __eq__(self, other):
        return self.name == other.name and \
            self.trello_id == other.trello_id and \
            self.color == other.color

    def to_json(self):
        return {
            'name': self.name,
            'trello_id': self.trello_id,
            'color': self.color
        }