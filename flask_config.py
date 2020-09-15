"""Flask configuration class."""
import os

class Config:
    """Base configuration variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Did you forget to run setup.sh?")
    
    API_PREFIX = 'https://api.trello.com/1/'
    API_KEY = os.getenv('API_KEY')
    API_TOKEN = os.getenv('API_TOKEN')
    API_PARAMS = {'key': API_KEY, 'token': API_TOKEN}
    board = os.getenv('BOARD_ID')
