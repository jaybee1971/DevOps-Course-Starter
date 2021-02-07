# DevOps Apprenticeship: Running Jason B's ToDo App

## Documentation

Can be found in the 'Documentation' folder and uses the C4 methodology (https://c4model.com/)
```bash
 * Context Diagram
 * Container Diagram
 * Component Diagram
 * Code level diagrams
```
Use the plantUML plugin for VSCode (or other IDEs) to generate code level diagrams from simple markdown.
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

## Trello API

The project uses the APIs from Trello.
To get this app to work for you, you will need to have a Trello account and store the following variables in your .env file (Use the .env.template to create your own entries from earlier step):
```bash
  * API_KEY  -  Your unique key for using the Trello API
  * API_TOKEN  -  Generate your own API token and store value here
  * BOARD_ID  -  The ID of the board you want to use for the project
```
For this application:
```bash
my_statuses = ["Not Started", "In Progress", "Completed"]
```
(this may differ from the Trello default statuses)

For this application, there are status column headings set in the .env as follows:

```bash
  * COL_1="Not Started"
  * COL_2="In Progress"
  * COL_3="Completed"
```

These differ from the Trello standard names and can be updated as needed.

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

To run Selenium you will need an appropriate driver for your browser of choice:
```bash
 * Firefox - Gecko Driver
 * Chrome - ChromeDriver from the Chromium project
```
Documentation and links can be found here:  https://www.selenium.dev/downloads/

Tests:
```bash
 * test_todos  -  unit tests for each class method
 * test_app  -  e2e system test with mocked Trello responses
 * test_browser  -  Selenium tests for launching app in different browsers (chrome test included)
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
 * $ poetry run pytest todo_app/browser_tests/firefox_test.py
(currently have to be run seperately)

Run all tests:
* $ sh test_suite.sh
```

## Using a Virtual Machine

This application can also be run within a virtual machine by using Vagrant.

Vagrant requires a hypervisor installed. We recommend VirtualBox.
https://www.virtualbox.org/

Download and install vagrant from the official website. You can check it's installed correctly by running the vagrant command in your terminal.
https://www.vagrantup.com/

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

Before using for your build, chnage the following:
```bash
 * Secure your Trello secure board tokens with your own Travis private key
 * Update the notifications section in the .travis.yml to your email address(es)
```

Goto https://travis-ci.com/ for more information on Travis
