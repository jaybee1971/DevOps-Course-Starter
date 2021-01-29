from datetime import datetime

class todo_item:

    def __init__(self, trello_id, title, description, due_date, status, last_updated):
        self.trello_id = trello_id
        self.title = title
        self.description = description
        self.due_date = self.format_due_date(due_date)
        self.status = status
        self.last_updated = self.format_updated(last_updated)


    def format_due_date(self, due_date):
        if due_date == None:
            return due_date
        else:
            iso_date = datetime.strptime(due_date, '%Y-%m-%dT%H:%M:%S.%fZ')
            return iso_date.strftime('%d/%m/%Y')


    def format_updated(self, last_updated):
        iso_date = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%S.%fZ')
        simple_date = iso_date.strftime('%d/%m/%Y')
        python_updated = datetime.strptime(simple_date, "%d/%m/%Y")
        return python_updated
         