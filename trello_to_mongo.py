import requests, pymongo, json

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
    todo = {
        '_id': item['id'],
        'name': item['name'],
        'desc': item['desc'],
        'due': item['due'],
        'status_id': item['idList'],
        'dateLastActivity': item['dateLastActivity']
    }
    todos.append(todo)


mongo_url = "your-mongo-url-here"
mongo_db = "your-db-name-here"

client = pymongo.MongoClient(mongo_url)
db = client[mongo_db]    

db.todo_items.insert_many( todos )

