import sys
import pytest
import dotenv
import todo_app.app
import requests, json


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


def mock_get(url, params):
    if url == 'https://api.trello.com/1/boards/test-trello-board-id/lists':
        return mock_statuses()
    else:
        # could qualify whole url for items and add else for failure
        return mock_items() 
 
           
def test_home_page(monkeypatch, client):
    monkeypatch.setattr(requests, "get", mock_get)
    response = client.get('/')
    
    assert response.status_code == 200
    assert "an item for testing with" in str(response.data)
    