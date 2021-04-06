# DevOps Apprenticeship: Running Jason B's ToDo App

## Heroku

The app is live hosted on Heroku:

https://jaybee1971-todoapp.herokuapp.com/


## Documentation

Can be found in the 'Documentation' folder and uses the C4 methodology (https://c4model.com/)
```bash
 * Context Diagram
 * Container Diagram
 * Component Diagram
 * Code level diagrams
```
Use the [plantUML](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml) plugin for VSCode (or other IDEs) to generate code level diagrams from simple markdown.

An example class_diagram.md for this application is included (and png of the diagram)


## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):


### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```


### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```


## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.


Check for additional dependencies

Packages required:
```bash
  * Requests
  * Pytest
  * Dotenv
  * Selenium
  * Gunicorn
```

To update any missing or new dependencies:
```bash
  $ poetry add <package_name>
```


## Mongo DB

The project uses a Mongo database from Atlas:
https://www.mongodb.com/


Configure the following environment variables for your db instance:
```bash
 * MONGO_URL="your-url"
 * MONGO_DB="your-database"
```

Previously the app used Trello and it's associated APIs.
If you want to convert previous Trello stored data to use Mongo, run this script to copy over your data:  ./trello_to_mongo.py


## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```

Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Running Tests

Ensure the dependencies are correct as per previous section.

To run [Selenium](https://www.selenium.dev/downloads/) you will need an appropriate driver for your browser of choice:
```bash
 * Firefox - Gecko Driver
 * Chrome - ChromeDriver from the Chromium project
```

Tests:
```bash
 * test_todos: Unit tests for each class method
 * test_app: End2end system test with mocked Trello responses
 * test_browser: Selenium tests for launching app in different browsers (chrome test included)
```

Running Tests:
```bash
Unit and System tests:
 * $ poetry run pytest todo_app/tests
      OR individually run as:
      * $ poetry run pytest todo_app/tests/test_todos.py
      * $ poetry run pytest todo_app/tests/test_app.py

Browser tests:
 * $ poetry run pytest todo_app/browser_tests/chrome_test.py

Run all tests:
* $ sh test_suite.sh
```


## Using a Virtual Machine

This application can also be run within a virtual machine by using Vagrant.

Vagrant requires a hypervisor installed. We recommend [VirtualBox](https://www.virtualbox.org/)

Download and install [Vagrant](https://www.vagrantup.com/) from the official website. You can check it's installed correctly by running the vagrant command in your terminal.

The Vagranfile within this repo will:
```bash
 * Pull down a Ubuntu Linux image to run the app
 * Prep your VM for Python installation
 * Install Python 3.8.5
 * Install poetry and load any dependencies
 * Launch the ToDo app
```

The VM can be managed using vagrant's CLI commands. Some useful ones are:
```bash
 * vagrant up - Starts your VM, creating and provisioning it automatically if required.
 * vagrant provision - Runs any VM provisioning steps specified in the Vagrantfile. Provisioning steps are one-off operations that adjust the system provided by the box.
 * vagrant suspend - Suspends any running VM. The VM will be restarted on the next vagrant up command.
 * vagrant destroy - Destroys the VM. It will be fully recreated the next time you run vagrant up.
```

Browse to the application from:  http://0.0.0.0:5000/


## Using Docker

This application can also be run within a Docker container, both as a production ready image, a development image and an image to just run tests.

Run the docker commands from the main application folder.

IMPORTANT:  
You will need different .env files for production versus development. Use the production .env for running the tests (as you need to open a link to Trello for the e2e system tests to work)

For production place the .env in your root and set the flask server config as:
```bash
# Flask server configuration.
FLASK_APP=todo_app.app
FLASK_ENV=production
```

For development place the .env in the todo_app directory and set the flask server config as:
```bash
# Flask server configuration.
FLASK_APP=app
FLASK_ENV=development
```

For a production ready container run:
```bash
$ docker-compose up --build
```
Image tag:  'todo-app:prod'
Container will run using gunicorn

For a development ready container run:
```bash
$ docker-compose --file docker-compose-dev.yml up --build
```
Image tag:  'todo-app:dev'
Container will run using the flask server and code can be updated and changes will reflect in the container

Browse to the application from:  http://0.0.0.0:5000/

For a container to run all tests only:
```bash
$ docker-compose --file docker-compose-test.yml up --build
```
Image tag:  'todo-app:test'
Container will run all the tests specified in 'entrypoint-test.sh' then stop


## Using Travis CI

This application can be built using Travis CI.

The following files are included for Travis:
```bash
 * .travis.yml
 * docker-compose-travis.yml
```

The included travis.yml will do the following:
```bash
 * only run CI new PRs are targetted to master
 * only run CD when there are merges to master
 * run tests against the test docker image
 * if tests pass (and this is a merge to master), build a new production image
 * push new image to docker hub
 * push new image to Heroku
```

Before using Travis for your build, change the following in the .travis.yml file:
```bash
 * Add any additional branches you want to auto build here: "(type = push AND branch IN (master)) OR (type = pull_request)"
 * Update any environment variables to meet your app needs (and remove any not needed)
 * Secure your Trello secure board tokens with your own Travis private key 
 * Update the notifications section to use your email address(es)
```

Goto https://travis-ci.com/ for more information on Travis
