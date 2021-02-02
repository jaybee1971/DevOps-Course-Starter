from flask import session, current_app as app
from todo_app.todo_item import todo_item
from todo_app.todo_status import todo_status
from todo_app.view_model import view_model
import os, requests, json, logging, sys


def trello_get(trello_path):
    return requests.get(app.config['API_PREFIX'] + trello_path, params=app.config['API_PARAMS'].copy()).json()


def get_trello_list_id(card_status):
    return [list_data.trello_id for list_data in get_trello_lists() if list_data.status == card_status][0]


def get_trello_lists():
    todo_statuses = []
    board = app.config['BOARD_ID']
    for item in trello_get(f'boards/{board}/lists'):
        list_data = todo_status(
            item['id'],
            item['name']
        )
        todo_statuses.append(list_data)
    return todo_statuses
    

def get_trello_cards():
    todo_items = []
    todo_statuses = get_trello_lists()
    for todo_status in todo_statuses:
        for item in trello_get(f'lists/{todo_status.trello_id}/cards'):
            todo = todo_item(
                item['id'],
                item['name'],
                item['desc'],
                item['due'],
                todo_status.status,
                item['dateLastActivity']
            )
            todo_items.append(todo)
    return todo_items


def trello_post(title, description, due_date):
    url = app.config['API_PREFIX'] + 'cards'
    post_params = app.config['API_PARAMS'].copy()
    post_params['name'] = title
    post_params['desc'] = description
    post_params['due'] = due_date
    post_params['idList'] = get_trello_list_id('Not Started')
    return requests.request(
        "POST", 
        url,
        params=post_params
    )


def trello_put(card_id, status):
    url = app.config['API_PREFIX'] + 'cards/' + card_id
    put_params = app.config['API_PARAMS'].copy()
    put_params['idList'] = get_trello_list_id(status)
    return requests.request(
        "PUT", 
        url,
        params=put_params
    )
 
  
def trello_delete(card_id):
    url = app.config['API_PREFIX'] + 'cards/' + card_id
    return requests.request(
        "DELETE", 
        url,
        params=app.config['API_PARAMS'].copy()
    )
 
 
def create_trello_board(api_key, api_token):
    create_params = (
        ('key', api_key),
        ('token', api_token),
        ('name', 'TestJbTodoApp')
    )    

    response = requests.post("https://api.trello.com/1/boards/", params=create_params)

    return response.json()['id']


def delete_trello_board(board_id, api_key, api_token):
    delete_params = (
        ('key', api_key),
        ('token', api_token)
    )
      
    requests.delete("https://api.trello.com/1/boards/" + board_id, params=delete_params)

  