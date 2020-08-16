from flask import session
from classes import trello_list, trello_card
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
        # list_data = trello_list(
        #     item['id'],
        #     item['name']
        # )
        list_data = {'trelloId': item['id'], 'status': item['name']}
        trelloLists.append(list_data)
        print(trelloLists)
    return trelloLists
    

def get_trello_cards():
    trelloCards = []
    id = 1
    trelloLists = get_trello_lists()
    for todoList in trelloLists:
        results = requests.get(API_PREFIX + 'lists/' + todoList['trelloId'] + '/cards', params={'key': API_KEY, 'token': API_TOKEN})
        trelloList = results.json()
        for item in trelloGet(f'boards/{board}/cards'):
            # todo = trello_card(
            #     item['id'],
            #     id,
            #     item['name'],
            #     todoList['status']
            # )
            todo = {'trelloId': item['id'], 'id': id, 'title': item['name'], 'status': todoList['status']}
            trelloCards.append(todo)
            id = id + 1
    return session.get('items', trelloCards)
