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
    return redirect('/')


@app.route('/update', methods=['POST'])
def update():
    for id in request.form:
        item = session.get_item(id)
        new_status = request.form.get(id)
        item['status'] = new_status
        session.save_item(item)
    return redirect('/')
    # I would add an if statement in this route to check status value
    # and if status was 'delete' would trigger new delete function
    # else it would update as above


if __name__ == '__main__':
    app.run()
