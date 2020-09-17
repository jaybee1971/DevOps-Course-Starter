from datetime import datetime

class todo_item:

    def __init__(self, trello_id, title, description, due_date, status):
        self.trello_id = trello_id
        self.title = title
        self.description = description
        self.due_date = self.format_date(due_date)
        self.status = status


    def format_date(self, due_date):
        if due_date == None:
            return due_date
        else:
            iso_date = datetime.strptime(due_date, '%Y-%m-%dT%H:%M:%S.%f%z')
            return iso_date.strftime("%d/%m/%Y")
        
        