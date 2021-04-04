import sys, os
import pytest, mongomock
import dotenv
import todo_app.app
import requests, json, pymongo
import datetime


file_mock_statuses = './todo_app/tests/mock_statuses.json'
file_mock_items = './todo_app/tests/mock_items.json'


@pytest.fixture
def client():
    file_path = './todo_app/tests/.env.test'
    dotenv.load_dotenv(file_path, override=True)
    test_app = todo_app.app.create_app()
    with test_app.test_client() as client:
        yield client


class Iterable(object):
    def __init__(self, list):
        self.list = list 
    def __iter__(self):
        for x in self.list:
            yield x

        
def mock_get_statuses():
    statuses = []
    with open(file_mock_statuses) as json_file_statuses:
        statuses = json_file_statuses.read().splitlines()
    return Iterable(statuses)


def mock_get_items():
    items = []
    with open(file_mock_items) as json_file_items:
        items = json_file_items.read().splitlines()
    return Iterable(items)
 

@mongomock.patch(servers=(("mongo", 12345),))    
def test_home_page(monkeypatch, client):
    import todo_app.app
    monkeypatch.setattr(todo_app.app, 'get_mongo_todo_statuses', mock_get_statuses)
    monkeypatch.setattr(todo_app.app, 'get_mongo_todo_items', mock_get_items)
    test_database()
    response = client.get('/')

    assert 'an item for testing with' in response.data.decode()


def test_database():
    client = pymongo.MongoClient(os.environ["MONGO_URL"])
    database = os.environ["MONGO_DB"]
    db = client.database
    db.test_todo_items.insert_one({"dateLastActivity": str(datetime.date.today()), "status_id": "5f2fb85702fda60cf038d800", "name": "an item for testing with"})
    