from flask import Flask, render_template, request, redirect, url_for
import session_items as session

app = Flask(__name__)
app.config.from_object('flask_config.Config')


@app.route('/', methods=['GET'])
def get_todo_list():
    todo_list = session.get_items()
    return render_template('index.html', items=todo_list)


@app.route('/create', methods=['POST'])
def create():
    session.add_item(request.form['add_todo'])
    return get_todo_list()


if __name__ == '__main__':
    app.run()
