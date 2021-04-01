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


class mock_statuses:
        
    @staticmethod   
    def json():
        with open(file_mock_statuses, 'r') as json_file_statuses:
            return json.load(json_file_statuses)

class mock_items:
        
    @staticmethod    
    def json():
        with open(file_mock_items, 'r') as json_file_items:
            return json.load(json_file_items)


def mock_get_statuses():
   return mock_statuses()


def mock_get_items():
    return mock_items() 
 

@mongomock.patch(servers=(("mongo", 12345),))    
def test_home_page(monkeypatch, client):
    import todo_app.mongo_db
    monkeypatch.setattr(todo_app.mongo_db, 'get_mongo_todo_statuses', mock_get_statuses)
    monkeypatch.setattr(todo_app.mongo_db, 'get_mongo_todo_items', mock_get_items)
    test_database()
    response = client.get('/')

    assert 'An item to test with' in response.data.decode()


def test_database():
    client = pymongo.MongoClient(os.environ["MONGO_URL"])
    database = os.environ["MONGO_DB"]
    db = client.database
    db.test_todo_items.insert_one({"last_modified": str(datetime.date.today()), "status_id": "abc1234567890", "name": "An item to test with"})
    