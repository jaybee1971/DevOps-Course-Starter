class todo_status:

    def __init__(self, trello_id, status):
        self.trello_id = trello_id
        self.status = status
        
    def __str__(self):
        return "({0}, {1})".format(self.trello_id, self.status)


class todo_item:

    def __init__(self, trello_id, title, description, due_date, status):
        self.trello_id = trello_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status


class view_model:
    
    my_statuses = ["Not Started", "In Progress", "Completed"]
    
    def __init__(self, todo_items, todo_statuses):
        self._todo_items = todo_items
        self._todo_statuses = todo_statuses
        
    @property
    def todo_items(self):
        return self._todo_items   
    
    @property
    def todo_statuses(self):
        return self._todo_statuses 
    
    def get_todo_statuses(self):
        return [todo_status for todo_status in self.todo_statuses if todo_status.status in view_model.my_statuses]
    
    def get_todo_status(self, status):
        return [todo_status for todo_status in self.todo_statuses if todo_status.status == status][0]
    
    def filter_by_todo_status(self, todo_status):
        return [todo_item for todo_item in self.todo_items if todo_item.status == todo_status.status]
    
    def filter_not_started_items(self):
        return self.filter_by_todo_status(self.get_todo_status(view_model.my_statuses[0]))

    def filter_in_progress_items(self):
        return self.filter_by_todo_status(self.get_todo_status(view_model.my_statuses[1]))     
    
    def filter_completed_items(self):
        return self.filter_by_todo_status(self.get_todo_status(view_model.my_statuses[2]))  
