import constants
import os
import parse
import time

from book import Book, BookEndpoints, Genre, GenreEndpoints
from client import ReadingQuantifiedClient
from dotenv import load_dotenv
from trello import TrelloClient

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
reading_quantified_client = ReadingQuantifiedClient(os.getenv('USERNAME'), os.getenv('PASSWORD'))
book_endpoints = BookEndpoints(reading_quantified_client)
genre_endpoints = GenreEndpoints(reading_quantified_client)

# Add label as Genre item
for label in labels:
    print(label)
    genre = Genre(
        label.name,
        label.id
    )
    response = genre_endpoints.post_genre(genre)
    print(response)
    time.sleep(2)

# For each item in the Finished List, add them to Reading Quantified
# TODO: Check if a card has already been added
for card in cards_in_finished_list:
    print(card)
    book = Book(
        card.name,
        card.id,
        parse.get_date_started(card),
        parse.get_date_finished(card),
        genres=card.idLabels
    )
    response = book_endpoints.post_book(book)
    print(response)

    # Wait a couple seconds before going onto the next card
    time.sleep(2)