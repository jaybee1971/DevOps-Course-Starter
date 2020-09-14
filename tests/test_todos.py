import pytest
from classes import todo_status, todo_item, view_model


test_items = [todo_item('00001', 'test item 1', 'item for testing', '', 'Not Started'),
              todo_item('00002', 'test item 2', 'item for testing', '', 'In Progress'),
              todo_item('00003', 'test item 3', 'item for testing', '', 'Completed'),
              todo_item('00004', 'test item 4', 'item for testing', '', 'Not Started'),
              todo_item('00005', 'test item 5', 'item for testing', '', 'In Progress'),
              todo_item('00006', 'test item 6', 'item for testing', '', 'Completed')
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
