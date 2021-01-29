#!/bin/bash

poetry run pytest todo_app/tests
wait
poetry run pytest todo_app/browser_tests/chrome_test.py
wait
poetry run pytest todo_app/browser_tests/firefox_test.py
