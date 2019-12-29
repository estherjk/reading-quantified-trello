from dotenv import load_dotenv
from trello import TrelloClient

import os
import time

# ## This project's imports

from books.client import ReadingQuantifiedClient
from books.models import Book, Genre

import books.constants as constants
import books.util as util

def sync_genres(trello_client, reading_quantified_client):
    """
    Synchronize the Reading Quantified Server with the genres (labels) listed in Trello.
    """

    # Get labels from Trello
    board = trello_client.get_board(constants.BOARD_ID)
    labels = board.get_labels()

    # Get all genres that exist on the Reading Quantified Server
    existing_genres = reading_quantified_client.get_genres()
    trello_ids = [ genre['trello_id'] for genre in existing_genres ]

    print('Syncing genres...')
    for label in labels:
        if label.id in trello_ids:
            # TODO: Update existing genre
            pass
        else:
            print('Adding new genre...')
            print(label)
            genre = Genre(
                label.name,
                label.id,
                color=label.color
            )
            response = reading_quantified_client.add_genre(genre)
            print(response)
    print('Done.')

def sync_books(trello_client, reading_quantified_client):
    """
    Synchronize the Reading Quantified Server with the finished books (cards in Finished list) on Trello.
    """
    
    # Get the cards with just the necessary info...
    finished_list = trello_client.get_list(constants.FINISHED_LIST_ID)
    cards_in_finished_list = finished_list.list_cards(
        actions=['createCard', 'updateCard:idList'],
        query={'attachments': 'cover'}
    )

    # Get all books that exist on the Reading Quantified Server
    existing_books = reading_quantified_client.get_books()
    trello_ids = [ book['trello_id'] for book in existing_books ]

    print('Syncing books...')
    for card in cards_in_finished_list:
        date_started = util.get_date_started(card)
        date_finished = util.get_date_finished(card)

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
            if card.id in trello_ids:
                # TODO: Update existing book
                pass
            else:
                print('Adding book...')
                print(card)
                response = reading_quantified_client.add_book(book)
                print(response)
    print('Done.')

def main():
    """
    Main!
    """
    load_dotenv()
    trello_client = TrelloClient(
        api_key=os.getenv('TRELLO_API_KEY')
    )
    reading_quantified_client = ReadingQuantifiedClient(os.getenv('BASE_URL'), os.getenv('USERNAME'), os.getenv('PASSWORD'))

    sync_genres(trello_client, reading_quantified_client)
    sync_books(trello_client, reading_quantified_client)

if __name__ == '__main__':
    main()