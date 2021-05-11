from flask_login import UserMixin

class TodoUser(UserMixin):
    def __init__(self, id):
        self.id = id
        self.role = self.get_role(self.id)
    
    def get_role(self, id):
        if id == "67792641":
            role = "writer"
        else:
            role = "reader"
        return role
            