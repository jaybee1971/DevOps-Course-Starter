from flask import Flask, render_template, request, redirect, url_for
import session_items as session
import os, requests, json
from operator import itemgetter

app = Flask(__name__)
app.config.from_object('flask_config.Config')

API_PREFIX = 'https://api.trello.com/1/'

API_KEY = os.getenv('API_KEY')
API_TOKEN = os.getenv('API_TOKEN')
board = os.getenv('BOARD_ID')

trelloLists = []
trelloToDos = []

@app.route('/trello', methods=['GET'])
def index():
    results = requests.get(API_PREFIX + 'boards/' + board + '/lists', params={'key': API_KEY, 'token': API_TOKEN})
    result = results.json()
    id = 1
    for item in result:
        list_data = {'id': item['id'], 'status': item['name']}
        trelloLists.append(list_data)
    for todoList in trelloLists:
        results = requests.get(API_PREFIX + 'lists/' + todoList['id'] + '/cards', params={'key': API_KEY, 'token': API_TOKEN})
        trelloList = results.json()
        for item in trelloList:
            todo = {'trelloId': item['id'], 'id': id, 'title': item['name'], 'status': todoList['status']}
            trelloToDos.append(todo)
            id = id + 1
    return f'{trelloToDos}'


@app.route('/', methods=['GET'])
def get_todo_list():
    todo_list = session.get_items()
    newlist = sorted(todo_list, key=itemgetter('status'), reverse=True)
    return render_template('index.html', items=newlist)


@app.route('/create', methods=['POST'])
def create():
    session.add_item(request.form['add_todo'])
    return redirect('/')


@app.route('/update', methods=['POST'])
def update():
    for id in request.form:
        new_status = request.form.get(id)
        if new_status == 'Delete':
            session.delete_item(id)
        else:
            item = session.get_item(id)
            old_status = item['status']
            if old_status == new_status:
                continue
            else:
                item['status'] = new_status
                session.save_item(item)
    return redirect('/')


if __name__ == '__main__':
    app.run()
