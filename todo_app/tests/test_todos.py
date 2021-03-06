import pytest
from todo_app.todo_item import todo_item
from todo_app.todo_status import todo_status
from todo_app.view_model import view_model
from datetime import *


today = datetime.today()
older1 = today - timedelta(1)
older2 = today - timedelta(2)
test_today = today.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
test_older1 = older1.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
test_older2 = older2.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

test_items = [todo_item('00001', 'test item 1', 'item for testing', None, 'Not Started', test_today),
              todo_item('00002', 'test item 2', 'item for testing', None, 'In Progress', test_today),
              todo_item('00003', 'test item 3', 'item for testing', None, 'Completed', test_today),
              todo_item('00004', 'test item 4', 'item for testing', None, 'Not Started', test_today),
              todo_item('00005', 'test item 5', 'item for testing', None, 'In Progress', test_today),
              todo_item('00006', 'test item 6', 'item for testing', None, 'Completed', test_older1),
              todo_item('00007', 'test item 7', 'item for testing', None, 'Completed', test_older1),
              todo_item('00008', 'test item 8', 'item for testing', None, 'Completed', test_older2),
              todo_item('00009', 'test item 9', 'item for testing', None, 'Completed', test_older2)
              ]

test_statuses = [todo_status('10000', 'Not Started'),
                 todo_status('20000', 'In Progress'),
                 todo_status('30000', 'Completed')
                 ]

my_statuses = ["Not Started", "In Progress", "Completed"]


@pytest.fixture 
def test_view_model():
    return view_model(test_items, test_statuses, my_statuses)


def test_get_todo_statuses(test_view_model):
    test_todo_statuses = test_view_model.get_todo_statuses()

    assert len(test_todo_statuses) == 3
    assert test_todo_statuses[0].status == test_statuses[0].status
    assert test_todo_statuses[1].status == test_statuses[1].status
    assert test_todo_statuses[2].status == test_statuses[2].status


def test_filter_not_started_items(test_view_model):
    test_not_started_items = test_view_model.filter_by_todo_status(test_statuses[0])

    assert test_not_started_items[0].mongo_id == test_items[0].mongo_id
    assert test_not_started_items[0].title == test_items[0].title
    assert test_not_started_items[1].mongo_id == test_items[3].mongo_id
    assert test_not_started_items[1].title == test_items[3].title


def test_filter_in_progress_items(test_view_model):
    test_in_progress_items = test_view_model.filter_by_todo_status(test_statuses[1])

    assert test_in_progress_items[0].mongo_id == test_items[1].mongo_id
    assert test_in_progress_items[0].title == test_items[1].title
    assert test_in_progress_items[1].mongo_id == test_items[4].mongo_id
    assert test_in_progress_items[1].title == test_items[4].title


def test_filter_completed_items(test_view_model):
    test_completed_items = test_view_model.filter_by_todo_status(test_statuses[2])

    assert test_completed_items[0].mongo_id == test_items[2].mongo_id
    assert test_completed_items[0].title == test_items[2].title
    assert test_completed_items[1].mongo_id == test_items[5].mongo_id
    assert test_completed_items[1].title == test_items[5].title


def test_older_items(test_view_model):
    test_older_completed_items = test_view_model.filter_older_completed_items()
    
    assert len(test_older_completed_items) ==  4
    

def test_newer_items(test_view_model):
    test_newer_completed_items = test_view_model.filter_newer_completed_items()
    
    assert len(test_newer_completed_items) ==  1    

        