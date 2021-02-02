import os, requests, json
import pytest
import todo_app.app
from selenium import webdriver
from todo_app.trello_api import create_trello_board, delete_trello_board
from threading import Thread
import dotenv
from dotenv import load_dotenv, find_dotenv


@pytest.fixture(scope='module')
def test_app():
    # Load .env
    filepath = find_dotenv('.env')
    load_dotenv(filepath, override=True)
    api_key = os.environ.get('API_KEY')
    api_token = os.environ.get('API_TOKEN')
    
    # Create the new board & update the board id environment variable
    test_board_id = create_trello_board(api_key, api_token)
    os.environ['BOARD_ID'] = test_board_id
    
    # Get the new board list ids and update the environment variables for the status column names
    setup_params = (
        ('key', api_key),
        ('token', api_token)
    )

    temp_lists = requests.get('https://api.trello.com/1/boards/' + os.environ['BOARD_ID'] + '/lists', params=setup_params)

    os.environ['COL_1'] = temp_lists.json()[0]['name']
    os.environ['COL_2'] = temp_lists.json()[1]['name']
    os.environ['COL_3'] = temp_lists.json()[2]['name']
    
    # construct the new application
    application = todo_app.app.create_app()
    
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    
    # Tear Down
    thread.join(1)
    delete_trello_board(test_board_id, api_key, api_token)


@pytest.fixture(scope='module') 
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome('./chromedriver', options=opts) as driver:
        yield driver


def test_python_home(driver, test_app): 
    driver.get("http://localhost:5000/")
    
    assert driver.title == 'Jason B To-Do App'
 