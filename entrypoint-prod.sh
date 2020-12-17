#!/bin/bash

poetry run gunicorn --config gunicorn_config.py 'todo_app.app:create_app()'
