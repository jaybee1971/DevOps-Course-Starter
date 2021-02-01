#!/bin/bash

poetry run pytest todo_app/tests/test_todos.py
wait
poetry run pytest todo_app/tests/test_app.py
# wait
# poetry run pytest todo_app/browser_tests/chrome_test.py
