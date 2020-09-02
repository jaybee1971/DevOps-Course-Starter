from flask import session
from classes import todo_status, todo_item
import os, requests, json, logging

API_PREFIX = 'https://api.trello.com/1/'

API_KEY = os.getenv('API_KEY')
API_TOKEN = os.getenv('API_TOKEN')
API_PARAMS = {'key': API_KEY, 'token': API_TOKEN}
board = os.getenv('BOARD_ID')


def trello_get(trello_path):
    return requests.get(API_PREFIX + trello_path, params=API_PARAMS.copy()).json()


def get_trello_list_id(card_status):
    return [list_data.trello_id for list_data in get_trello_lists() if list_data.status == card_status][0]


def get_trello_lists():
    trello_lists = []
    for item in trello_get(f'boards/{board}/lists'):
        list_data = todo_status(
            item['id'],
            item['name']
        )
        trello_lists.append(list_data)
    return trello_lists
    

def get_trello_cards():
    trello_cards = []
    trello_lists = get_trello_lists()
    for todo_list in trello_lists:
        for item in trello_get(f'lists/{todo_list.trello_id}/cards'):
            todo = todo_item(
                item['id'],
                item['name'],
                item['desc'],
                item['due'],
                todo_list.status
            )
            trello_cards.append(todo)
    return trello_cards


def trello_post(title, description, due_date):
    url = API_PREFIX + 'cards'
    post_params = API_PARAMS.copy()
    post_params['idList'] = get_trello_list_id('Not Started')
    post_params['name'] = title
    post_params['desc'] = description
    post_params['due'] = due_date
    return requests.request(
        "POST", 
        url,
        params=post_params
    )


def trello_put(card_id, status):
    url = API_PREFIX + 'cards/' + card_id
    put_params = API_PARAMS.copy()
    put_params['idList'] = get_trello_list_id(status)
    return requests.request(
        "PUT", 
        url,
        params=put_params
    )
 
  
def trello_delete(card_id):
    url = API_PREFIX + 'cards/' + card_id
    return requests.request(
        "DELETE", 
        url,
        params=API_PARAMS.copy()
    )
      