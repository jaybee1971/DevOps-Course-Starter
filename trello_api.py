from flask import session
from classes import todoStatus, todoItem
import os, requests, json

API_PREFIX = 'https://api.trello.com/1/'

API_KEY = os.getenv('API_KEY')
API_TOKEN = os.getenv('API_TOKEN')
API_PARAMS = {'key': API_KEY, 'token': API_TOKEN}
board = os.getenv('BOARD_ID')
headers = {"Accept": "application/json"}


def trelloGet(trelloPath):
    return requests.get(API_PREFIX + trelloPath, params=API_PARAMS).json()


def get_trello_lists():
    trelloLists = []
    for item in trelloGet(f'boards/{board}/lists'):
        list_data = todoStatus(
            item['id'],
            item['name']
        )
        trelloLists.append(list_data)
        if list_data.status == "Not Started":
            session['newItemId'] = list_data.trelloId
        if list_data.status == "In Progress":
            session['progressId'] = list_data.trelloId
        if list_data.status == "Completed":
            session['completedId'] = list_data.trelloId
    return trelloLists
    

def get_trello_cards():
    trelloCards = []
    trelloLists = get_trello_lists()
    for todoList in trelloLists:
        for item in trelloGet(f'lists/{todoList.trelloId}/cards'):
            todo = todoItem(
                item['id'],
                item['name'],
                todoList.status
            )
            trelloCards.append(todo)
    return trelloCards


def trelloPost(title):
    url = API_PREFIX + '/cards'
    newParams = API_PARAMS
    newParams['idList'] = str(session['newItemId'])
    newParams['name'] = title
    return requests.request(
        "POST", 
        url,
        params=newParams
    )


def trelloPut(cardId, status):
    url = API_PREFIX + '/cards/' + cardId
    newParams = API_PARAMS
    if status == 'Not Started':
        newParams['idList'] = str(session['newItemId'])
    if status == 'In Progress':
        newParams['idList'] = str(session['progressId'])
    if status == 'Completed':
        newParams['idList'] = str(session['completedId'])
    return requests.request(
        "PUT", 
        url,
        headers=headers,
        params=newParams
    )
 
  
def trelloDelete(cardId):
    url = API_PREFIX + '/cards/' + cardId
    return requests.request(
        "DELETE", 
        url,
        params=API_PARAMS
    )
      