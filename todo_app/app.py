import logging, os, sys, requests
from datetime import datetime
from operator import itemgetter
from flask_login import login_required, login_user, current_user
import todo_app.login_manager as login_manager
from oauthlib.oauth2 import WebApplicationClient
from flask import Flask, redirect, render_template, request, url_for

from todo_app.flask_config import Config
from todo_app.todo_user import TodoUser
from todo_app.todo_item import todo_item
from todo_app.todo_status import todo_status
from todo_app.mongo_db import (get_todo_items, get_list_id,
                                 get_todo_statuses, database_delete, todo_get,
                                 database_post, database_put)
from todo_app.view_model import view_model


def create_app():
    app = Flask(__name__)
    # uncomment to debug
    # logging.basicConfig(level=logging.DEBUG)
    app.config.from_object(Config())
    login_manager.login_manager.init_app(app)
    
    # All the routes and setup code etc
    @app.route('/')
    @login_required
    def index():
        if app.config["LOGIN_DISABLED"] == "True":
            user_role = "writer"
        else:
            user_role = current_user.role
        my_statuses = app.config['STATUSES']
        todo_list = view_model(get_todo_items(),get_todo_statuses(), my_statuses)
        app.logger.info('Processing get cards request')
        return render_template('index.html', view_model_items=todo_list, view_role=user_role)


    @app.route('/create', methods=['POST'])
    @login_required
    def new_todo():
        if app.config["LOGIN_DISABLED"] == "True" or current_user.role == "writer":
            last_update = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            database_post(request.form['add_todo'], request.form['add_desc'], request.form['due_date'], last_update)
            app.logger.info('Processing create new card request')
            return index()
        else:
            return index()


    @app.route('/update', methods=['POST'])
    @login_required
    def update():
        if app.config["LOGIN_DISABLED"] == "True" or current_user.role == "writer":
            for mongo_id in request.form:
                card_status = request.form.get(mongo_id)
                if card_status == 'Delete':
                    database_delete(mongo_id)
                    app.logger.info('Processing delete card request')
                else:
                    last_update = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                    database_put(mongo_id, card_status, last_update)
                    app.logger.info('Processing update card request')
            return index()
        else:
            return index()
    
    
    @app.route('/login/callback')
    def login_callback():
        app.logger.info('OAuth')
        callback_code = request.args.get("code")
        
        gh_client =  WebApplicationClient(app.config['GH_CLIENT_ID'])
        
        gh_token = gh_client.prepare_token_request(
            "https://github.com/login/oauth/access_token",
            code=callback_code
        ) 
        
        gh_access = requests.post(
            gh_token[0], 
            headers=gh_token[1], 
            data=gh_token[2], 
            auth=(app.config['GH_CLIENT_ID'], 
            app.config['GH_SECRET'])
        )
        
        gh_json = gh_client.parse_request_body_response(gh_access.text)
        
        gh_request_param = gh_client.add_token(uri="https://api.github.com/user")
        
        gh_user_info = requests.get(
            gh_request_param[0],
            headers=gh_request_param[1]
        ).json()
        
        login_user(TodoUser(gh_user_info['id']))
                   
        return index()

    return app

if __name__ == '__main__':
    create_app().run()
    