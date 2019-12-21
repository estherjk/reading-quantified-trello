from dotenv import load_dotenv
from trello import TrelloClient

import os
import time

# This project's imports

from books.book import Book, BookEndpoints, Genre, GenreEndpoints
from books.client import ReadingQuantifiedClient

import books.constants as constants
import books.parse as parse

load_dotenv()

# Trello Client
trello_client = TrelloClient(
    api_key=os.getenv('TRELLO_API_KEY')
)
finished_list = trello_client.get_list(constants.FINISHED_LIST_ID)
cards_in_finished_list = finished_list.list_cards(actions=['createCard', 'updateCard:idList'])
board = trello_client.get_board(constants.BOARD_ID)
labels = board.get_labels()

# Reading Quantified Client
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

# Add a book to Reading Quantified
print('Adding new books...')

for card in cards_in_finished_list:
    date_started = parse.get_date_started(card)
    date_finished = parse.get_date_finished(card)

    if card.id not in trello_ids and date_started and date_finished:
        print(card)
        book = Book(
            card.name,
            card.id,
            date_started,
            date_finished,
            genres=card.idLabels
        )
        response = book_endpoints.post_book(book)
        print(response)

print('Done.')