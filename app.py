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
not_started = os.getenv('COL_1')


@app.route('/trello', methods=['GET'])
def index():
    results = requests.get(API_PREFIX + 'lists/' + not_started + '/cards', params={'key': API_KEY, 'token': API_TOKEN})
    result = results.json()
    return f'{result}'


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
