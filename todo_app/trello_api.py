from flask import session, current_app as app
from todo_app.todo_item import todo_item
from todo_app.todo_status import todo_status
from todo_app.view_model import view_model
import os, requests, json, logging, sys, pymongo


def mongo_todo_get(status_id):
    mongo_url = app.config['MONGO_URL']
    mongo_db = app.config['MONGO_DB']
    
    client = pymongo.MongoClient(mongo_url)
    db = client[mongo_db]
    items = db.todo_items
    items.find({'status_id': status_id})


def get_trello_list_id(card_status):
    return [list_data.trello_id for list_data in get_mongo_todo_statuses() if list_data.status == card_status][0]


def get_mongo_todo_statuses():
    todo_statuses = []
    mongo_url = app.config['MONGO_URL']
    mongo_db = app.config['MONGO_DB']
    
    client = pymongo.MongoClient(mongo_url)
    db = client[mongo_db]
    statuses = db.todo_statuses
    for status in statuses.find():
        list_data = todo_status(
            status['_id'],
            status['name']
        )
        todo_statuses.append(list_data)
    
    return todo_statuses
      

def get_mongo_todo_items():
    todo_items = []
    todo_statuses = get_mongo_todo_statuses()
    for todo_status in todo_statuses:
        for item in mongo_todo_get(todo_status.trello_id):
            todo = todo_item(
                item['_id'],
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

  