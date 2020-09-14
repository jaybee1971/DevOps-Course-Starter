from flask import Flask, render_template, request, redirect, url_for
import logging
from classes import todo_status, todo_item, view_model
from trello_api import trello_get, get_trello_list_id, get_trello_lists, get_trello_cards, trello_post, trello_put, trello_delete
from operator import itemgetter

app = Flask(__name__)
# uncomment to debug API calls
# logging.basicConfig(level=logging.DEBUG)
app.config.from_object('flask_config.Config')


@app.route('/', methods=['GET'])
def get_trello_todo_list():
    trello_todo_list = view_model(get_trello_cards())
    app.logger.info('Processing get cards request')
    return render_template('index.html', view_model_items=trello_todo_list)


@app.route('/create', methods=['POST'])
def new_todo():
    trello_post(request.form['add_todo'], request.form['add_desc'], request.form['due_date'])
    app.logger.info('Processing create new card request')
    return redirect('/')


@app.route('/update', methods=['POST'])
def update():
    for trello_id in request.form:
        card_status = request.form.get(trello_id)
        if card_status == 'Delete':
            trello_delete(trello_id)
            app.logger.info('Processing delete card request')
        else:
            trello_put(trello_id, card_status)
            app.logger.info('Processing update card request')
    return redirect('/')


if __name__ == '__main__':
    app.run()
