from flask_login import UserMixin

class TodoUser(UserMixin):
    
    writer = "writer"
    reader = "reader"
    
    def __init__(self, id):
        self.id = id
        self.role = TodoUser.writer if id == "67792641" else TodoUser.reader
              