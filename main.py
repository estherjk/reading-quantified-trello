from dotenv import load_dotenv
from trello import TrelloClient

import os
import time

# ## This project's imports

from books.book import Book, BookEndpoints, Genre, GenreEndpoints
from books.client import ReadingQuantifiedClient

import books.constants as constants
import books.parse as parse

load_dotenv()

# ## Trello Books board

trello_client = TrelloClient(
    api_key=os.getenv('TRELLO_API_KEY')
)
finished_list = trello_client.get_list(constants.FINISHED_LIST_ID)
board = trello_client.get_board(constants.BOARD_ID)
labels = board.get_labels()

# Get the cards with just the necessary info...
cards_in_finished_list = finished_list.list_cards(
    actions=['createCard', 'updateCard:idList'],
    query={'attachments': 'cover'}
)

# ## Reading Quantified Client

reading_quantified_client = ReadingQuantifiedClient(os.getenv('BASE_URL'), os.getenv('USERNAME'), os.getenv('PASSWORD'))
book_endpoints = BookEndpoints(reading_quantified_client)
genre_endpoints = GenreEndpoints(reading_quantified_client)

# Get all genres that exist in Reading Quantified
existing_genres = genre_endpoints.get_genres()
trello_ids = [ genre['trello_id'] for genre in existing_genres ]

# Add label as Genre item
print('Adding new genres...')
for label in labels:
    if label.id not in trello_ids:
        print(label)
        genre = Genre(
            label.name,
            label.id
        )
        response = genre_endpoints.post_genre(genre)
        print(response)
print('Done.')

# Get all books that exist in Reading Quantified
existing_books = book_endpoints.get_books()
trello_ids = [ book['trello_id'] for book in existing_books ]

# Add books to Reading Quantified
print('Adding new books...')
for card in cards_in_finished_list:
    date_started = parse.get_date_started(card)
    date_finished = parse.get_date_finished(card)

    # The cards have been filtered for just the cover attachment, but it's stored in a list.
    cover_attachment = card.attachments[0] if card.attachments else {}

    book = Book(
        card.name,
        card.id,
        date_started,
        date_finished,
        genres=card.idLabels,
        cover_attachment=cover_attachment
    )
    
    if date_started and date_finished:
        if card.id not in trello_ids:
            print('Adding book...')
            print(card)
            response = book_endpoints.post_book(book)
            print(response)
        else:
            # Existing books are missing cover attachment info... let's add it.
            # TODO: Updating books should be more generic?
            data = book_endpoints.get_books(query_params={'trello_id': card.id})
            if not data[0]['cover_attachment'] and cover_attachment:
                print('Updating book...')
                response = book_endpoints.put_book(data[0]['url'], book)
                print(response)

print('Done.')