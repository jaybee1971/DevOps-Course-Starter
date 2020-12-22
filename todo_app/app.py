import logging
import os
import sys
from datetime import datetime
from operator import itemgetter

from flask import Flask, redirect, render_template, request, url_for

from todo_app.flask_config import Config
from todo_app.todo_item import todo_item
from todo_app.todo_status import todo_status
from todo_app.trello_api import (get_trello_cards, get_trello_list_id,
                                 get_trello_lists, trello_delete, trello_get,
                                 trello_post, trello_put)
from todo_app.view_model import view_model


def create_app():
    app = Flask(__name__)
    # uncomment to debug API calls
    logging.basicConfig(level=logging.DEBUG)
    app.config.from_object(Config())
    
    # All the routes and setup code etc
    @app.route('/', methods=['GET'])
    def get_trello_todo_list():
        trello_todo_list = view_model(get_trello_cards(),get_trello_lists())
        app.logger.info('Processing get cards request')
        return render_template('index.html', view_model_items=trello_todo_list)


    @app.route('/create', methods=['POST'])
    def new_todo():
        if request.form['due_date'] == '':
            trello_date = ''
        else:
            trello_date = datetime.strptime(request.form['due_date'], '%d/%m/%Y')
        trello_post(request.form['add_todo'], request.form['add_desc'], trello_date)
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

    return app

if __name__ == '__main__':
    create_app().run()
