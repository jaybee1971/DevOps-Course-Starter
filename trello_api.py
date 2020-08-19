from flask import session
from classes import todoStatus, todoItem
import os, requests, json

API_PREFIX = 'https://api.trello.com/1/'

API_KEY = os.getenv('API_KEY')
API_TOKEN = os.getenv('API_TOKEN')
API_PARAMS = {'key': API_KEY, 'token': API_TOKEN}
board = os.getenv('BOARD_ID')


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
    id = 1
    trelloLists = get_trello_lists()
    for todoList in trelloLists:
        for item in trelloGet(f'lists/{todoList.trelloId}/cards'):
            todo = todoItem(
                item['id'],
                id,
                item['name'],
                todoList.status
            )
            trelloCards.append(todo)
            id = id + 1
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
