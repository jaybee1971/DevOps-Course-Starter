import os, requests, json
from pathlib import Path
import pytest, pymongo
import todo_app.app
from selenium import webdriver
from threading import Thread
import dotenv
from dotenv import load_dotenv, find_dotenv


@pytest.fixture(scope='module')
def test_app():
    # Load .env if file exists
    if Path('.env').exists() is True:
        filepath = dotenv.find_dotenv('.env')
        dotenv.load_dotenv(filepath, override=True)
    
    # disable GitHub OAuth
    os.environ['LOGIN_DISABLED'] = "True"
    
    # construct the new application
    application = todo_app.app.create_app()
    
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    
    # Tear Down
    thread.join(1)


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
 