import pytest
import todo_app.app
from selenium import webdriver

@pytest.fixture(scope='module')
def test_app():
# Create the new board & update the board id environment variable (need to create this function)
    board_id = create_trello_board()
    os.environ['TRELLO_BOARD_ID'] = board_id
    # construct the new application
    application = todo_app.app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    # Tear Down
    thread.join(1)
    # need to create this function
    delete_trello_board(board_id)

@pytest.fixture(scope='module') 
def driver():
    with webdriver.Chrome() as driver:
        yield driver


def test_python_home(driver): 
    driver.get("http://localhost:5000/")
    assert driver.title == 'Jason B To-Do App'
 