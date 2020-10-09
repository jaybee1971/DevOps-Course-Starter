import pytest
from todo_item import todo_item
from todo_status import todo_status
from view_model import view_model
from datetime import *


today = datetime.today()
older1 = today - timedelta(1)
older2 = today - timedelta(2)
test_today = today.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
test_older1 = older1.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
test_older2 = older2.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

test_items = [todo_item('00001', 'test item 1', 'item for testing', None, 'Not Started', ''),
              todo_item('00002', 'test item 2', 'item for testing', None, 'In Progress', ''),
              todo_item('00003', 'test item 3', 'item for testing', None, 'Completed', test_today),
              todo_item('00004', 'test item 4', 'item for testing', None, 'Not Started', ''),
              todo_item('00005', 'test item 5', 'item for testing', None, 'In Progress', ''),
              todo_item('00006', 'test item 6', 'item for testing', None, 'Completed', test_older1),
              todo_item('00007', 'test item 7', 'item for testing', None, 'Completed', test_older1),
              todo_item('00008', 'test item 8', 'item for testing', None, 'Completed', test_older2)
              ]

test_statuses = [todo_status('10000', 'Not Started'),
                 todo_status('20000', 'In Progress'),
                 todo_status('30000', 'Completed')
                 ]


@pytest.fixture 
def test_view_model():
    return view_model(test_items, test_statuses)


def test_get_todo_statuses(test_view_model):
    test_todo_statuses = test_view_model.get_todo_statuses()

    assert len(test_todo_statuses) == 3
    assert test_todo_statuses[0].status == test_statuses[0].status
    assert test_todo_statuses[1].status == test_statuses[1].status
    assert test_todo_statuses[2].status == test_statuses[2].status


def test_filter_not_started_items(test_view_model):
    test_not_started_items = test_view_model.filter_by_todo_status(test_statuses[0])

    assert test_not_started_items[0].trello_id == test_items[0].trello_id
    assert test_not_started_items[0].title == test_items[0].title
    assert test_not_started_items[1].trello_id == test_items[3].trello_id
    assert test_not_started_items[1].title == test_items[3].title


def test_filter_in_progress_items(test_view_model):
    test_in_progress_items = test_view_model.filter_by_todo_status(test_statuses[1])

    assert test_in_progress_items[0].trello_id == test_items[1].trello_id
    assert test_in_progress_items[0].title == test_items[1].title
    assert test_in_progress_items[1].trello_id == test_items[4].trello_id
    assert test_in_progress_items[1].title == test_items[4].title


def test_filter_completed_items(test_view_model):
    test_completed_items = test_view_model.filter_by_todo_status(test_statuses[2])

    assert test_completed_items[0].trello_id == test_items[2].trello_id
    assert test_completed_items[0].title == test_items[2].title
    assert test_completed_items[1].trello_id == test_items[5].trello_id
    assert test_completed_items[1].title == test_items[5].title


def test_completed_by_date(test_view_model):
    test_completed_today = test_view_model.filter_completed_by_date(test_today)
    test_completed_yesterday = test_view_model.filter_completed_by_date(test_older1)
    test_completed_older = test_view_model.filter_completed_by_date(test_older2)
    
    assert test_completed_today[0].last_updated ==  test_items[2].last_updated
    assert test_completed_yesterday[0].last_updated ==  test_items[5].last_updated
    assert test_completed_yesterday[0].last_updated ==  test_items[6].last_updated
    assert test_completed_older[0].last_updated ==  test_items[7].last_updated
    