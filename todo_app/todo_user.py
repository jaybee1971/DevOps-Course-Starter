from flask_login import UserMixin

class todo_user(UserMixin):
    def __init__(self, user_id):
        self.id = user_id['id']
        self.login = user_id['login']
        self.role = self.get_role(self.login)
    
    def get_role(self, login):
        if login == "jaybee1971":
            role = "writer"
        else:
            role = "reader"
        return role
            