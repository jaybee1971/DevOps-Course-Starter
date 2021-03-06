"""Flask configuration class."""
import os

class Config:
    def __init__(self):
        """Base configuration variables."""
        self.LOGIN_DISABLED = os.getenv('LOGIN_DISABLED')
        self.SECRET_KEY = os.getenv('SECRET_KEY')
        self.GH_CLIENT_ID = os.getenv('GH_CLIENT_ID')
        self.GH_SECRET = os.getenv('GH_SECRET')
        self.MONGO_URL = os.getenv('MONGO_URL')
        self.MONGO_DB = os.getenv('MONGO_DB')
        self.STATUSES = ["Not Started", "In Progress", "Completed"]
