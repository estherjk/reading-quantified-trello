import os

from dotenv import load_dotenv
from trello import TrelloClient

load_dotenv()

client = TrelloClient(
    api_key=os.getenv('TRELLO_API_KEY')
)

books_board = client.get_board('564d07a87721d8698ff010d3')
print(books_board.name)