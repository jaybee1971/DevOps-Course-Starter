from datetime import datetime

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
    
    def recent_completed_items(self):
        done_list = filter_completed_items()
        today = datetime.date.today()
        recent_items = [todo_item for todo_item in done_list if todo_item.last_updated.date() == today]
        return recent_items
