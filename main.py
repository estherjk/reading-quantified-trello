import os

import constants
import parse

from dotenv import load_dotenv
from trello import TrelloClient

load_dotenv()

client = TrelloClient(
    api_key=os.getenv('TRELLO_API_KEY')
)

finished_list = client.get_list(constants.FINISHED_LIST_ID)
cards_in_finished_list = finished_list.list_cards(actions=['createCard', 'updateCard:idList'])

# TEST
card_index = 51

date_started = parse.get_date_started(cards_in_finished_list[card_index])
print(date_started)

date_finished = parse.get_date_finished(cards_in_finished_list[card_index])
print(date_finished)