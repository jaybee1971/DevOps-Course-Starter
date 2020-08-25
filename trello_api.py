from flask import session
from classes import todo_status, todo_item
import os, requests, json, logging

API_PREFIX = 'https://api.trello.com/1/'

API_KEY = os.getenv('API_KEY')
API_TOKEN = os.getenv('API_TOKEN')
API_PARAMS = {'key': API_KEY, 'token': API_TOKEN}
board = os.getenv('BOARD_ID')
headers = {"Accept": "application/json"}


def trello_get(trelloPath):
    return requests.get(API_PREFIX + trelloPath, params=API_PARAMS.copy()).json()


def get_trello_lists():
    trello_lists = []
    for item in trello_get(f'boards/{board}/lists'):
        list_data = todo_status(
            item['id'],
            item['name']
        )
        trello_lists.append(list_data)
        if list_data.status == "Not Started":
            session['newItemId'] = list_data.trello_id
        if list_data.status == "In Progress":
            session['progressId'] = list_data.trello_id
        if list_data.status == "Completed":
            session['completedId'] = list_data.trello_id
    return trello_lists
    

def get_trello_cards():
    trello_cards = []
    trello_lists = get_trello_lists()
    for todoList in trello_lists:
        for item in trello_get(f'lists/{todoList.trello_id}/cards'):
            todo = todo_item(
                item['id'],
                item['name'],
                item['desc'],
                todoList.status
            )
            trello_cards.append(todo)
    return trello_cards


def trello_post(title, description):
    url = API_PREFIX + 'cards'
    post_params = API_PARAMS.copy()
    post_params['idList'] = str(session['newItemId'])
    post_params['name'] = title
    post_params['desc'] = description
    return requests.request(
        "POST", 
        url,
        params=post_params
    )


def trello_put(cardId, status):
    url = API_PREFIX + 'cards/' + cardId
    put_params = API_PARAMS.copy()
    if status == 'Not Started':
        put_params['idList'] = str(session['newItemId'])
    if status == 'In Progress':
        put_params['idList'] = str(session['progressId'])
    if status == 'Completed':
        put_params['idList'] = str(session['completedId'])
    return requests.request(
        "PUT", 
        url,
        headers=headers,
        params=put_params
    )
 
  
def trello_delete(cardId):
    url = API_PREFIX + 'cards/' + cardId
    return requests.request(
        "DELETE", 
        url,
        params=API_PARAMS.copy()
    )
      