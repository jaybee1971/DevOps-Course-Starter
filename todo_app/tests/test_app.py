import sys, os
import pytest
import dotenv
import todo_app.app
import requests, json

dir = os.path.dirname(__file__)
file_mock_statuses = os.path.join(dir, 'mock_statuses.json')
file_mock_items = os.path.join(dir, 'mock_items.json')


@pytest.fixture
def client():
    file_path = dotenv.find_dotenv('.env.test')
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


def mock_get(*args, **kwargs):
    return mock_statuses()
    return mock_items()
                           
                           
def test_home_page(monkeypatch, client):
    monkeypatch.setattr(requests, "get", mock_get)
    response = client.get('/')
    
    assert response.status_code == 200
    assert "an item for testing with" in str(response.data)
    