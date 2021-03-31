from datetime import datetime

class todo_item:

    def __init__(self, mongo_id, title, description, due_date, status, last_updated):
        self.mongo_id = mongo_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status
        self.last_updated = self.format_updated(last_updated)


    def format_updated(self, last_updated):
        iso_date = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%S.%fZ')
        simple_date = iso_date.strftime('%d/%m/%Y')
        python_updated = datetime.strptime(simple_date, "%d/%m/%Y")
        return python_updated
         