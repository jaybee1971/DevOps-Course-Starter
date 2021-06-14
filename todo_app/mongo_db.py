from flask import session, current_app as app
from todo_app.todo_item import todo_item
from todo_app.todo_status import todo_status
from todo_app.view_model import view_model
import os, requests, json, logging, sys, pymongo
from bson import ObjectId


# As per comments from module 10 exercise, the bespoke statuses approach was not really working
# Therefore created a fixed file of statuses to replace any database call for now
# Will refactor statuses entirely at some point
file_statuses = './todo_app/statuses.json'


def todo_get(status_id):
    todo_items = []
    mongo_url = app.config['MONGO_URL']
    mongo_db = app.config['MONGO_DB']
    
    client = pymongo.MongoClient(mongo_url)
    db = client[mongo_db]
    collection = db.todo_items
    todo_items = collection.find({'status_id': status_id})
    
    return todo_items


def get_list_id(card_status):
    return [list_data.mongo_id for list_data in get_todo_statuses() if list_data.status == card_status][0]


def get_todo_statuses():
    todo_statuses = []
    with open(file_statuses) as json_file_statuses:
        status_collection = json.load(json_file_statuses)
        for status in status_collection:
            list_data = todo_status(
                status['_id'],
                status['name']
            )
            todo_statuses.append(list_data)
    return todo_statuses
      

def get_todo_items():
    todo_items = []
    todo_statuses = get_todo_statuses()
    for todo_status in todo_statuses:
        for item in todo_get(todo_status.mongo_id):
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


def database_post(title, description, due_date, last_update):
    new_todo = {
        '_id': ObjectId(),
        'name': title,
        'desc': description,
        'due': str(due_date),
        'status_id': get_list_id('Not Started'),
        'dateLastActivity': last_update
    }
        
    mongo_url = app.config['MONGO_URL']
    mongo_db = app.config['MONGO_DB']
    
    client = pymongo.MongoClient(mongo_url)
    db = client[mongo_db]
    collection = db.todo_items
    collection.insert_one(new_todo)


def database_put(card_id, status, last_update):
    updated_todo = {"$set": 
        {
        'status_id': get_list_id(status),
        'dateLastActivity': last_update
        }
    }
        
    mongo_url = app.config['MONGO_URL']
    mongo_db = app.config['MONGO_DB']
    
    client = pymongo.MongoClient(mongo_url)
    db = client[mongo_db]
    collection = db.todo_items
    
    dbquery = {"_id": ObjectId(card_id)}
    
    collection.update_one(dbquery, updated_todo)
 
  
def database_delete(card_id):
    mongo_url = app.config['MONGO_URL']
    mongo_db = app.config['MONGO_DB']

    client = pymongo.MongoClient(mongo_url)
    db = client[mongo_db]
    collection = db.todo_items

    dbquery = {"_id": ObjectId(card_id)}

    collection.delete_one(dbquery) 
      