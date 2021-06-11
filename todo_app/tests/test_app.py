import sys, os
import pytest, mongomock
import dotenv
import todo_app.app
from todo_app.todo_item import todo_item
from todo_app.todo_status import todo_status
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

        
def mock_get_statuses():
    mock_statuses = []
    with open(file_mock_statuses) as json_file_statuses:
        mock_collection = json.load(json_file_statuses)
        for status in mock_collection:
            list_data = todo_status(
                status['_id'],
                status['name']
            )
            mock_statuses.append(list_data)
    return mock_statuses


def mock_get_items():
    mock_items = []
    with open(file_mock_items) as json_file_items:
        mock_collection = json.load(json_file_items)
        for item in mock_collection:
            todo = todo_item(
                item['_id'],
                item['name'],
                item['desc'],
                item['due'],
                item['status_id'],
                item['dateLastActivity']
            )
            mock_items.append(todo)
    return mock_items


def mock_database():
    client = pymongo.MongoClient(os.environ["MONGO_URL"])
    database = os.environ["MONGO_DB"]
    db = client.database
    db.test_todo_items.insert_one({"dateLastActivity": str(datetime.date.today()), "status_id": "5f2fb85702fda60cf038d800", "name": "an item for testing with"})
   

@mongomock.patch(servers=(("mongo", 12345),))    
def test_home_page(monkeypatch, client):
    import todo_app.app
    monkeypatch.setattr(todo_app.app, 'get_todo_statuses', mock_get_statuses)
    monkeypatch.setattr(todo_app.app, 'get_todo_items', mock_get_items)
    mock_database()
    response = client.get('/')

    assert 'an item for testing with' in response.data.decode()
