import os
import trello


SITE_BOARD_ID = "XwByypgs"

class TrelloClientManager(object):

    def __init__(self):
        # Setup client with API key and read/write token
        self.client = trello.TrelloApi(os.environ.get("TRELLO_KEY"), os.environ.get("TRELLO_SECRET"))
        self.client.set_token(os.environ.get("TRELLO_TOKEN"))

    def get_board(self):
        return self.client.get_board(SITE_BOARD_ID)

    def get_lists(self):
        return self.client.get_list(SITE_BOARD_ID)

    def get_cards(self):
        return client.boards.get_card(SITE_BOARD_ID)

    