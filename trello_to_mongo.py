import requests, pymongo, json
from bson import ObjectId
from datetime import *


trello_items = []

url = "https://api.trello.com/1/boards/{your-board-id-here}/cards"

query = {
   'key': 'your-trello-key-here',
   'token': 'your-trello-token-here'
}

trello_items = requests.request(
   "GET",
   url,
   params=query
)

items = trello_items.json()

todo = {}
todos = []

for item in items:
    iso_date = datetime.strptime(item['due'], '%Y-%m-%dT%H:%M:%S.%fZ')
    mongo_date = iso_date.strftime('%d/%m/%Y')
    todo = {
        '_id': ObjectId(),
        'name': item['name'],
        'desc': item['desc'],
        'due': mongo_date,
        'status_id': item['idList'],
        'dateLastActivity': item['dateLastActivity']
    }
    todos.append(todo)


mongo_url = "your-mongo-url-here"
mongo_db = "your-db-name-here"

client = pymongo.MongoClient(mongo_url)
db = client[mongo_db]    

db.todo_items.insert_many( todos )

# Add default statuses (update your own column names and substitute ObjectID for Trello idList value if importing data from Trello)
db.todo_statuses.insert_many([
  { '_id': ObjectId(), 'name': 'Not Started' },
  { '_id': ObjectId(), 'name': 'In Progress' },
  { '_id': ObjectId(), 'name': 'Completed' }
])

