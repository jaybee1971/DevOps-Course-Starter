import os
import pytest
import todo_app.app
from selenium import webdriver
from todo_app.trello_api import create_trello_board, delete_trello_board
from threading import Thread
import dotenv
import requests


@pytest.fixture(scope='module')
def test_app():
    
    # Create the new board & update the board id environment variable
    test_board_id = create_trello_board()
    os.environ['BOARD_ID'] = test_board_id
    
    # construct the new application
    application = todo_app.app.create_app()
    
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    
    # Tear Down
    thread.join(1)
    delete_trello_board(test_board_id)


@pytest.fixture(scope='module') 
def driver():
    with webdriver.Firefox() as driver:
        yield driver


def test_python_home(driver, test_app): 
    driver.get("http://localhost:5000/")
    assert driver.title == 'Jason B To-Do App'
    