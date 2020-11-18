# DevOps Apprenticeship: Running Jason B's ToDo App

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
```

To update any missing dependencies:
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

This application can also be run within a Docker container.

From the main application folder:
```bash
$ docker-compose up --build
```

Browse to the application from:  http://0.0.0.0:5000/
