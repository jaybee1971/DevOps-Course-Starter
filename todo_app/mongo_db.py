from flask import session, current_app as app
from todo_app.todo_item import todo_item
from todo_app.todo_status import todo_status
from todo_app.view_model import view_model
import os, requests, json, logging, sys, pymongo
from bson import ObjectId


def mongo_todo_get(status_id):
    todo_items = []
    mongo_url = app.config['MONGO_URL']
    mongo_db = app.config['MONGO_DB']
    
    client = pymongo.MongoClient(mongo_url)
    db = client[mongo_db]
    collection = db.todo_items
    todo_items = collection.find({'status_id': status_id})
    
    return todo_items


def get_mongo_list_id(card_status):
    return [list_data.mongo_id for list_data in get_mongo_todo_statuses() if list_data.status == card_status][0]


def get_mongo_todo_statuses():
    todo_statuses = []
    mongo_url = app.config['MONGO_URL']
    mongo_db = app.config['MONGO_DB']
    
    client = pymongo.MongoClient(mongo_url)
    db = client[mongo_db]
    collection = db.todo_statuses
    for status in collection.find():
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
        for item in mongo_todo_get(todo_status.mongo_id):
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


def mongo_post(title, description, due_date, last_update):
    new_todo = {
        '_id': ObjectId(),
        'name': title,
        'desc': description,
        'due': str(due_date),
        'status_id': get_mongo_list_id('Not Started'),
        'dateLastActivity': last_update
    }
        
    mongo_url = app.config['MONGO_URL']
    mongo_db = app.config['MONGO_DB']
    
    client = pymongo.MongoClient(mongo_url)
    db = client[mongo_db]
    collection = db.todo_items
    collection.insert_one(new_todo)


def mongo_put(card_id, status, last_update):
    updated_todo = {"$set": 
        {
        'status_id': get_mongo_list_id(status),
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
 
  
def mongo_delete(card_id):
    mongo_url = app.config['MONGO_URL']
    mongo_db = app.config['MONGO_DB']

    client = pymongo.MongoClient(mongo_url)
    db = client[mongo_db]
    collection = db.todo_items

    dbquery = {"_id": ObjectId(card_id)}

    collection.delete_one(dbquery) 
      