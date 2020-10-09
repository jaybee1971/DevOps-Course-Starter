"""Flask configuration class."""
import os

class Config:
    def __init__(self):
        """Base configuration variables."""
        self.API_PREFIX = 'https://api.trello.com/1/'
        self.API_KEY = os.getenv('API_KEY')
        self.API_TOKEN = os.getenv('API_TOKEN')
        self.API_PARAMS = {'key': self.API_KEY, 'token': self.API_TOKEN}
        self.BOARD_ID = os.getenv('BOARD_ID')
