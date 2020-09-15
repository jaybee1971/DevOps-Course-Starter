from flask import session
from flask_config import Config
from classes import todo_status, todo_item, view_model
import os, requests, json, logging, sys


def trello_get(trello_path):
    return requests.get(Config.API_PREFIX + trello_path, params=Config.API_PARAMS.copy()).json()


def get_trello_list_id(card_status):
    return [list_data.trello_id for list_data in get_trello_lists() if list_data.status == card_status][0]


def get_trello_lists():
    todo_statuses = []
    for item in trello_get(f'boards/{Config.board}/lists'):
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
                todo_status.status
            )
            todo_items.append(todo)
    return todo_items


def trello_post(title, description, due_date):
    url = Config.API_PREFIX + 'cards'
    post_params = Config.API_PARAMS.copy()
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
    url = Config.API_PREFIX + 'cards/' + card_id
    put_params = Config.API_PARAMS.copy()
    put_params['idList'] = get_trello_list_id(status)
    return requests.request(
        "PUT", 
        url,
        params=put_params
    )
 
  
def trello_delete(card_id):
    url = Config.API_PREFIX + 'cards/' + card_id
    return requests.request(
        "DELETE", 
        url,
        params=Config.API_PARAMS.copy()
    )
      