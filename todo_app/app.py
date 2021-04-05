import logging
import os
import sys
from datetime import datetime
from operator import itemgetter

from flask import Flask, redirect, render_template, request, url_for

from todo_app.flask_config import Config
from todo_app.todo_item import todo_item
from todo_app.todo_status import todo_status
from todo_app.mongo_db import (get_mongo_todo_items, get_mongo_list_id,
                                 get_mongo_todo_statuses, mongo_delete, mongo_todo_get,
                                 mongo_post, mongo_put)
from todo_app.view_model import view_model


def create_app():
    app = Flask(__name__)
    # uncomment to debug
    # logging.basicConfig(level=logging.DEBUG)
    app.config.from_object(Config())
    
    # All the routes and setup code etc
    @app.route('/', methods=['GET'])
    def get_mongo_todo_list():
        my_statuses = app.config['STATUSES']
        mongo_todo_list = view_model(get_mongo_todo_items(),get_mongo_todo_statuses(), my_statuses)
        app.logger.info('Processing get cards request')
        return render_template('index.html', view_model_items=mongo_todo_list)


    @app.route('/create', methods=['POST'])
    def new_todo():
        last_update = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        mongo_post(request.form['add_todo'], request.form['add_desc'], request.form['due_date'], last_update)
        app.logger.info('Processing create new card request')
        return redirect('/')


    @app.route('/update', methods=['POST'])
    def update():
        for mongo_id in request.form:
            card_status = request.form.get(mongo_id)
            if card_status == 'Delete':
                print(mongo_id)
                mongo_delete(mongo_id)
                app.logger.info('Processing delete card request')
            else:
                last_update = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                mongo_put(mongo_id, card_status, last_update)
                app.logger.info('Processing update card request')
        return redirect('/')

    return app

if __name__ == '__main__':
    create_app().run()
