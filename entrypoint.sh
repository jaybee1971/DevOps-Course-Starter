#!/bin/bash

poetry run gunicorn --config gunicorn_config.py 'app:create_app()'
