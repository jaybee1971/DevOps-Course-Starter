"""Flask configuration class."""
import os

class Config:
    def __init__(self):
        """Base configuration variables."""
        self.MONGO_URL = os.getenv('MONGO_URL')
        self.MONGO_DB = os.getenv('MONGO_DB')
        self.API_PREFIX = 'https://api.trello.com/1/'
        self.API_KEY = os.getenv('API_KEY')
        self.API_TOKEN = os.getenv('API_TOKEN')
        self.API_PARAMS = {'key': self.API_KEY, 'token': self.API_TOKEN}
        self.BOARD_ID = os.getenv('BOARD_ID')
        self.COL_1 = os.getenv('COL_1')
        self.COL_2 = os.getenv('COL_2')
        self.COL_3 = os.getenv('COL_3')
        self.STATUSES = [self.COL_1, self.COL_2, self.COL_3]
