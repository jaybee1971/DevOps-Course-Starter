from flask_login import LoginManager
from flask import session, redirect, current_app as app
from oauthlib.oauth2 import WebApplicationClient
import requests
import os
from todo_app.todo_user import todo_user


login_manager = LoginManager()
@login_manager.unauthorized_handler
def unauthenticated():
    gh_client =  WebApplicationClient(app.config['GH_CLIENT_ID'])
    gh_redirect = gh_client.prepare_request_uri("https://github.com/login/oauth/authorize")

    return redirect(gh_redirect) 
         
@login_manager.user_loader
def load_user(user_id):
    return None
