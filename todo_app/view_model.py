from datetime import *
import dateutil.parser
import os

class view_model:
    
    today = datetime.today()
    format_today = today.strftime('%d/%m/%Y')
    python_today = datetime.strptime(format_today, "%d/%m/%Y")
    
    def __init__(self, todo_items, todo_statuses, my_statuses):
        self._todo_items = todo_items
        self._todo_statuses = todo_statuses
        self._my_statuses = my_statuses
        
    @property
    def todo_items(self):
        return self._todo_items   
    
    @property
    def todo_statuses(self):
        return self._todo_statuses 
    
    @property
    def my_statuses(self):
        return self._my_statuses 
    
    def get_todo_statuses(self):
        return [todo_status for todo_status in self.todo_statuses if todo_status.status in self.my_statuses]
    
    def get_todo_status(self, status):
        return [todo_status for todo_status in self.todo_statuses if todo_status.status == status][0]
    
    def filter_by_todo_status(self, todo_status):
        return [todo_item for todo_item in self.todo_items if todo_item.status == todo_status.status]
    
    def filter_not_started_items(self):
        return self.filter_by_todo_status(self.get_todo_status(self.my_statuses[0]))

    def filter_in_progress_items(self):
        return self.filter_by_todo_status(self.get_todo_status(self.my_statuses[1]))     
    
    def filter_completed_items(self):
        return self.filter_by_todo_status(self.get_todo_status(self.my_statuses[2]))  
    
    def filter_older_completed_items(self):
        done_list = self.filter_completed_items()
        if len(done_list) < 5:
            older_completed_items = []
            return older_completed_items
        else:
            older_completed_items = [todo_item for todo_item in done_list if todo_item.last_updated < self.python_today]
            return older_completed_items
    
    def filter_newer_completed_items(self):
        done_list = self.filter_completed_items()
        if len(done_list) < 5:
            return done_list
        else:
            newer_completed_items = [todo_item for todo_item in done_list if todo_item.last_updated >= self.python_today]
            return newer_completed_items
