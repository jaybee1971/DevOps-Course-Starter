import pytest, dotenv, todo_app


@pytest.fixture
def client():
    file_path = dotenv.find_dotenv('.env.test')
    dotenv.load_dotenv(file_path, override=True)
    test_app = todo_app.create_app()
    with test_app.test_client() as client:
        yield client

        
def test_index_page(mock_get_requests, client):
    response = client.get('/')
 