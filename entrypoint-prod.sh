#!/bin/bash

poetry run gunicorn --config gunicorn_config.py --bind 0.0.0.0:${PORT:-5000} 'todo_app.app:create_app()'
