import pytest
from selenium import webdriver


@pytest.fixture(scope='module') 
def driver():
    with webdriver.Chrome() as driver:
        yield driver


def test_python_home(driver): 
    driver.get("http://localhost:5000/")
    assert driver.title == 'Jason B To-Do App'
    